import os
import sys
import time
import random

try:
    import pylibmc
    MEMCACHED_LOADED = True
except ImportError:
    MEMCACHED_LOADED = False

################################################################################
################################################################################
################################################################################

class PdsCache(object):

        pass

################################################################################
################################################################################
################################################################################

class DictionaryCache(PdsCache):

    def __init__(self, lifetime=86400, limit=1000, logger=None):
        """Constructor.

        Input:
            lifetime        default lifetime in seconds; 0 for no expiration.
                            Can be a constant or a function; if the latter, then
                            the default lifetime must be returned by this call:
                                lifetime(value)
            limit           limit on the number of items in the cache. Permanent
                            objects do not count against this limit.
            logger          PdsLogger to use, optional.
        """

        self.dict = {}              # returns (value, expiration) by key
        self.keys = set()           # set of non-permanent keys

        if type(lifetime).__name__ == 'function':
            self.lifetime_func = lifetime
            self.lifetime = None
        else:
            self.lifetime = lifetime
            self.lifetime_func = None

        self.limit = limit
        self.slop = max(20, self.limit/10)
        self.logger = logger

        self.pauses = 0

    def _trim(self):
        """Trim the dictionary if it is too big."""

        if len(self.keys) > self.limit + self.slop:
            expirations = [(self.dict[k][1], k) for k in self.keys if
                            self.dict[k][1] is not None]
            expirations.sort()
            pairs = expirations[:-self.limit]
            for (_, key) in pairs:
                del self.dict[key]
                self.keys.remove(key)

            if self.logger:
                self.logger.debug('%d items trimmed from DictionaryCache' %
                                  len(pairs))

    def _trim_if_necessary(self):
        if self.pauses == 0:
            self._trim()

    def flush(self):
        """Flush any buffered items. Not used for DictionaryCache."""
        return

    def block(self):
        """Block any process from touching the cache. Not used by
        DictionaryCache."""
        return

    def unblock(self, flush=True):
        """Un-block processes from touching the cache. Not used by
        DictionaryCache."""
        return

    def is_blocked(self):
        """Status of blocking. Not used by DictionaryCache."""
        return False

    def pause(self):
        """Increment the pause count. Trimming will resume when the count
        returns to zero."""

        self.pauses += 1
        if self.pauses == 1 and self.logger:
            self.logger.debug('DictionaryCache trimming paused')

    @property
    def is_paused(self):
        """Report on status of automatic trimming."""

        return self.pause > 0

    def resume(self):
        """Decrement the pause count. Trimming will resume when the count
        returns to zero."""

        if self.pauses > 0:
            self.pauses -= 1

        if self.pauses == 0:
            self._trim()
            if self.logger:
                self.logger.debug('DictionaryCache trimming resumed')

    def __contains__(self, key):
        """Enable the "in" operator."""
        return (key in self.dict)

    def __len__(self):
        """Enable len() operator."""

        return len(self.dict)

    ######## Get methods

    def get(self, key):
        """Return the value associated with a key. Return None if the key is
        missing."""

        if key not in self.dict:
            return None

        (value, expiration) = self.dict[key]

        if expiration is None:
            return value

        if expiration < time.time():
            del self[key]
            return None

        return value

    def __getitem__(self, key):
        """Enable dictionary syntax. Raise KeyError if the key is missing."""

        value = self.get(key)
        if value is None:
            raise KeyError(key)

        return value

    def get_multi(self, keys):
        """Return a dictionary of multiple values based on a list of keys.
        Missing keys do not appear in the returned dictionary."""

        mydict = {}
        for key in keys:
            value = self[key]
            if value is not None:
                mydict[key] = value

        return mydict

    def get_local(self, key):
        """Return the value associated with a key, only using the local dict."""

        return self.get(key)

    def get_now(self, key):
        """Return the non-local value associated with a key."""

        return self.get(key)

    ######## Set methods

    def set(self, key, value, lifetime=None, pause=False):
        """Set the value associated with a key.

        lifetime    the lifetime of this item in seconds; 0 for no expiration;
                    None to use the default lifetime.
        pause       True to postpone any trim operation.
        """

        # Determine the expiration time
        if lifetime is None:
            if self.lifetime:
                lifetime = self.lifetime
            else:
                lifetime = self.lifetime_func(value)

        if lifetime == 0:
            expiration = None
        else:
            expiration = time.time() + lifetime

        # Save in the dictionary
        self.dict[key] = (value, expiration)
        if expiration:
            self.keys.add(key)

        # Trim if necessary
        if not pause:
            self._trim_if_necessary()

    def __setitem__(self, key, value):
        """Enable dictionary syntax."""

        self.set(key, value)

    def set_multi(self, mydict, lifetime=0, pause=False):
        """Set multiple values at one time based on a dictionary."""

        for (key, value) in mydict.items():
            self.set(key, value, lifetime, pause=True)

        if not pause:
            self._trim_if_necessary()

        return []

    def set_local(self, key, value, lifetime=None):
        """Just like set() but always goes to the local dictionary without
        touching the cache."""

        return self.set(key, value, lifetime=lifetime)

    ######## Delete methods

    def delete(self, key):
        """Delete one key. Return true if it was deleted, false otherwise."""

        if key in self.dict:
            del self.dict[key]
            return True

        return False

    def __delitem__(self, key):
        """Enable the "del" operator. Raise KeyError if the key is absent."""

        if key in self.dict:
            del self.dict[key]
            return

        raise KeyError(key)

    def delete_multi(self, keys):
        """Delete multiple items based on a list of keys. Keys not found in
        the cache are ignored. Returns True if all keys were deleted."""

        status = True
        for key in keys:
            if key in self.dict:
                del self.dict[key]
            else:
                status = False

        return status

    def clear(self, block=False):
        """Clear all concents of the cache."""

        self.dict.clear()
        self.keys = set()

    def replicate_clear(self, clear_count):
        """Clear the local cache if clear_count was incremented.

        Return True if cache was cleared; False otherwise.
        """

        return False

    def replicate_clear_if_necessary(self):
        """Clear the local cache only if MemCache was cleared."""

        return

    def was_cleared(self):
        """Returns True if the cache has been cleared."""

        return False

################################################################################
################################################################################
################################################################################

class MemcachedCache(PdsCache):

    def __init__(self, port=11211, lifetime=86400, localsize=10, localtime=60,
                                   logger=None):
        """Constructor.

        Input:
            port            port number for the memcache, which must already
                            have been established. Alternatively, the absolute
                            path to a Unix socket.
            lifetime        default lifetime in seconds; 0 for no expiration.
                            Can be a constant or a function; if the latter, then
                            the default lifetime must be returned by
                                lifetime(self)
            localsize       number of items to accumulate in an internal
                            dictionary before they are flushed to the memcache.
            localtime       limits on the number of seconds an item should
                            remain in the buffer before it is flushed to the
                            memcache.
            logger          PdsLogger to use, optional.
        """

        self.port = port

        if type(port) == str:
            self.mc = pylibmc.Client([port], binary=True)
        else:
            self.mc = pylibmc.Client(['127.0.0.1:%d' % port], binary=True)

        if type(lifetime).__name__ == 'function':
            self.lifetime_func = lifetime
            self.lifetime = None
        else:
            self.lifetime = int(lifetime + 0.999)
            self.lifetime_func = None

        self.localsize = localsize
        self.localtime = localtime
        self.flushtime = 0.

        self.local_value_by_key = {}
        self.local_lifetime_by_key = {}
        self.local_keys_by_lifetime = {}
        # local_values_by_key is an internal dictionary of values that have not
        # yet been flushed to memcache.
        # local_lifetime_by_key is an internal dictionary of their lifetimes in
        # seconds, using the same key.
        # local_keys_by_lifetime is the inverse dictionary, which returns a list
        # of keys given a lifetime value.

        self.pauses = 0
        # This counter is incremented for every call to pause() and decremented
        # by every call to resume(). Flushing will not occur unless this value
        # is zero. Note that pauses can be nested, which is why it is a counter
        # and not a flag.

        self.permanent_values = {}
        # This is an internal copy of all values that this thread has
        # encountered lifetime == 0. It is used for extra protection in case
        # memcache allows a permanent value to expire.

        self.toobig_dict = {}
        # Any object that triggers a "TooBig" error is stored inside this
        # internal dictionary. It is not removed from memcached (if there)
        # because other threads might still use it, but this thread will never
        # again try to retrieve it from memcached. As a result, this dictionary
        # has to be the first place to look for any key.

        self.logger = logger

        # Test the cache with a random key so as not to clobber existing keys
        while True:
            key = str(random.randint(0,10**40))
            if key in self.mc:
                continue

            self.mc[key] = 1
            del self.mc[key]
            break

        # Save the ID of this process
        self.pid = os.getpid()

        # Initialize as unblocked
        if len(self) == 0:
            self.mc.set('$OK_PID', 0, time=0)
        # When the cached value of '$OK_PID' is nonzero, it means that the
        # thread with this process ID is currently blocking it.

        # Get the current count of clear() events and save it internally
        self.clear_count = self.mc.get('$CLEAR_COUNT')
        if self.clear_count is None:
            self.clear_count = 0
            self.mc.set('$CLEAR_COUNT', 0, time=0)
        # This is the internal copy of the cached value of '$CLEAR_COUNT'. When
        # a thread clears the cache, this value is incremented. If this thread
        # finds a cached value that differs from its internal value, it knows
        # to clear its own contents.

    def block(self):
        """Block any other process from touching the cache."""

        # Wait for a block to clear if necessary
        if self.is_blocked():
            block_was_logged = False
            while self.is_blocked():
                if not block_was_logged and self.logger:
                    self.logger.info(f'Process {self.pid} is blocked at ' +
                                     f'block() on MemcacheCache [{self.port}]')
                    block_was_logged = True
                time.sleep(0.5 * (1. + random.random()))  # A random short delay

            if block_was_logged and self.logger:
                self.logger.info(f'Process {self.pid} is unblocked at ' +
                                 f'block() on MemcacheCache [{self.port}]')

        self.mc.set('$OK_PID', self.pid, time=60)
        if self.logger:
            self.logger.info(f'Process {self.pid} is blocking '
                             f'MemcachedCache [{self.port}]')

    def unblock(self, flush=True):
        """Remove block preventing processes from touching the cache."""

        test_pid = self.mc.get('$OK_PID')
        if test_pid == 0:
            if self.logger:
                self.logger.error(f'Process {self.pid} is unable to unblock ' +
                                  f'MemcachedCache [{self.port}]; ' +
                                  f'Cache is already unblocked')
                return

        if test_pid != self.pid:
            if self.logger:
                self.logger.error(f'Process {self.pid} is unable to unblock ' +
                                  f'MemcachedCache [{self.port}]; ' +
                                  f'Cache is blocked by process {test_pid}')
                return

        if flush:
            self.flush()
        else:
            self._flush_if_necessary()

        self.mc.set('$OK_PID', 0, time=0)

        if self.logger:
            self.logger.info(f'Process {self.pid} removed block of ' +
                             f'MemcachedCache [{self.port}]')

    def is_blocked(self):
        """Status of blocking."""

        test_dict = self.mc.get_multi(['$OK_PID', '$CLEAR_COUNT'])
        self.replicate_clear(test_dict['$CLEAR_COUNT'])

        test_pid = test_dict['$OK_PID']
        if test_pid in (0, self.pid):
            return False
        else:
            return True

    def pause(self):
        """Increment the pause count. Flushing will resume when this count
        returns to zero."""
        self.pauses += 1

        if self.pauses == 1 and self.logger:
            self.logger.debug(f'Process {self.pid} has paused flushing on ' +
                              f'MemcachedCache [{self.port}]')

    @property
    def is_paused(self):
        """Report on status of automatic flushing for this thread."""

        return self.pause > 0

    def resume(self):
        """Decrement the pause count. Flushing of this thread will resume when
        the count returns to zero."""

        if self.pauses > 0:
            self.pauses -= 1

        if self.pauses == 0:
            if self.logger:
                self.logger.debug(f'Process {self.pid} has resumed flushing ' +
                                  f'on MemcachedCache [{self.port}]')
            self._flush_if_necessary()

    def __contains__(self, key):
        """Enable the "in" operator."""

        if key in self.local_value_by_key: return True
        if key in self.permanent_values: return True
        if key in self.toobig_dict: return True

        block_was_logged = False
        while self.is_blocked():
            if not block_was_logged and self.logger:
                self.logger.info(f'Process {self.pid} is blocked at ' +
                                 f'contains() on MemcachedCache [{self.port}]')
                block_was_logged = True
            time.sleep(0.5 * (1. + random.random()))  # A random short delay

        if block_was_logged and self.logger:
            self.logger.info(f'Process {self.pid} is unblocked at contains() ' +
                             f'on MemcachedCache [{self.port}]')

        return key in self.mc

    def __len__(self):
        """Enable len() operator."""

        items = self.len_mc()

        for key in self.toobig_dict:
            if key not in self.mc:
                items += 1

        for key in self.local_value_by_key:
            if key not in self.mc:
                items += 1

        return items

    def len_mc(self):
        return int(self.mc.get_stats()[0][1]['curr_items'])

    ######## Flush methods

    def flush(self, wait=False):
        """Flush any buffered items into the cache."""

        # Nothing to do if local cache is empty
        if len(self.local_value_by_key) == 0:
            return

        # Wait for a block to clear if necessary
        if self.is_blocked():
          if wait:
            block_was_logged = False
            while self.is_blocked():
                if not block_was_logged and self.logger:
                    self.logger.info(f'Process {self.pid} is blocked at ' +
                                     f'flush() on MemcacheCache [{self.port}]')
                    block_was_logged = True
                time.sleep(0.5 * (1. + random.random()))  # A random short delay

            if block_was_logged and self.logger:
                self.logger.info(f'Process {self.pid} is unblocked at ' +
                                 f'flush() on MemcacheCache [{self.port}]')

          # Otherwise, save changes for later
          else:
            return

        if self.replicate_clear_if_necessary():
            return

        # Save non-expiring values to the permanent dictionary
        if 0 in self.local_keys_by_lifetime:
            for k in self.local_keys_by_lifetime[0]:
                self.permanent_values[k] = self.local_value_by_key[k]

        # Cache items grouped by lifetime
        failures = []
        toobigs = []
        for lifetime in self.local_keys_by_lifetime:

            # Save tuples (value, lifetime)
            mydict = {k:(self.local_value_by_key[k], lifetime) for
                                    k in self.local_keys_by_lifetime[lifetime]}

            # Update to memcache
            try:
                self.mc.set_multi(mydict, time=lifetime)
            except pylibmc.TooBig:  # comes up with big HTML pages
                for (k,v) in mydict.items():
                  try:
                    self.mc.set(k, v, time=lifetime)
                  except pylibmc.TooBig:
                    toobigs.append(k)
                    failures.append(k)
                    self.toobig_dict[k] = v
                    if self.logger:
                      self.logger.warn(f'TooBig error in process {self.pid}; ' +
                                       f'saved to internal cache', k)
            except pylibmc.Error as e:
                if self.logger:
                    self.logger.exception(e)

                keys = mydict.keys()
                if self.logger:
                    keys.sort()
                    for key in keys:
                      self.logger.error(f'Process {self.pid} has failed to ' +
                                        f'flush; deleted', key)

                failures += keys

        if self.logger:
            count = len(self.local_keys_by_lifetime) - len(failures)
            if count == 1:
                desc = '1 item,'
            else:
                desc = str(count) + ' items, including'
            self.logger.debug(f'Process {self.pid} has flushed {desc} ' +
                              list(mydict.keys())[0] +
                              f', to MemcachedCache [{self.port}]; ' +
                              f'current size is {self.len_mc()}')
            if toobigs:
                count = len(self.toobig_dict)
                noun = 'item' if count == 1 else 'items'
                self.logger.debug(f'Process {self.pid} now has {count} big ' +
                                  f'{noun} cached locally')

        # Clear internal dictionaries
        self.local_lifetime_by_key.clear()
        self.local_value_by_key.clear()
        self.local_keys_by_lifetime.clear()

    def _flush_if_necessary(self):
        if self.pauses > 0: return

        if (len(self.local_value_by_key) > self.localsize or
            time.time() > self.flushtime):
                self.flush(wait=False)

    ######## Get methods

    def get(self, key):
        """Return the value associated with a key. Return None if the key is
        missing."""

        # Return from local caches if found
        if key in self.toobig_dict:
            return self.toobig_dict[key]

        if key in self.local_value_by_key:
            return self.local_value_by_key[key]

        # Otherwise, go to Memcache but wait for block
        key_and_ok = ['$OK_PID', '$CLEAR_COUNT', key]
        mydict = self.mc.get_multi(key_and_ok)

        self.replicate_clear(mydict['$CLEAR_COUNT'])

        block_was_logged = False
        while '$OK_PID' not in mydict or mydict['$OK_PID'] not in (0, self.pid):
            if not block_was_logged and self.logger:
                self.logger.info(f'Process {self.pid} is blocked at get() on ' +
                                 f'MemcacheCache [{self.port}]')
                block_was_logged = True
            time.sleep(0.5 * (1. + random.random()))  # A random short delay
            mydict = self.mc.get_multi(key_and_ok)

        if block_was_logged and self.logger:
            self.logger.info(f'Process %d is unblocked at get() on ' +
                             f'MemcacheCache [{self.port}]')

        # Return value from memcache if found
        if key in mydict:
            (value, lifetime) = mydict[key]

            # Save permanent values in local dictionary
            if lifetime == 0:
                self.permanent_values[key] = value

            return value

        # Check the permanent dictionary in case it was deleted from memcache
        if key in self.permanent_values:
            self._restore_permanent_to_cache()
            return self.permanent_values[key]

        return None

    def __getitem__(self, key):
        """Enable dictionary syntax. Raise KeyError if the key is missing."""

        value = self.get(key)
        if value is None:
            raise KeyError(key)

        return value

    def get_multi(self, keys):
        """Return a dictionary of multiple values based on a list or set of
        keys. Missing keys do not appear in the returned dictionary."""

        # Separate keys into local, toobig, and non-local (in memcache)
        nonlocal_keys = set(keys)
        toobig_keys = set(self.toobig_dict.keys()) & nonlocal_keys
        nonlocal_keys -= toobig_keys

        local_keys = set(self.local_value_by_key.keys()) & nonlocal_keys
        nonlocal_keys -= local_keys

        # Retrieve non-local keys if any
        if nonlocal_keys:
            keys_and_ok = ['$OK_PID', '$CLEAR_COUNT'] + nonlocal_keys
            block_was_logged = False
            mydict = self.mc.get_multi(keys_and_ok)

            self.replicate_clear(mydict['$CLEAR_COUNT'])

            while ('$OK_PID' not in mydict or
                   mydict['$OK_PID'] not in (0, self.pid)):

                if not block_was_logged and self.logger:
                    self.logger.info(f'Process {self.pid} is blocked at ' +
                                     f'get_multi() on ' +
                                     f'MemcacheCache [{self.port}]')
                    block_was_logged = True
                time.sleep(0.5 * (1. + random.random()))  # A random short delay
                mydict = self.mc.get_multi(keys_and_ok)

            if block_was_logged and self.logger:
                self.logger.info(f'Process {self.pid} is unblocked at ' +
                                 f'get_multi() on MemcacheCache [{self.port}]')

            for (key, tuple) in mydict.items():
                (value, lifetime) = tuple
                mydict[key] = value

                # Save permanent values in local dictionary
                if lifetime == 0:
                    self.permanent_values[key] = value

            # Restore any permanent values missing from memcache
            for key in nonlocal_keys:
                if key in self.permanent_values:
                    self._restore_permanent_to_cache()
                    break

        else:
            mydict = {}

        # Retrieve local keys if any
        for key in toobig_keys:
            mydict[key] = self.toobig_dict[key]

        for key in local_keys:
            mydict[key] = self.local_value_by_key[key]

        return mydict

    def get_local(self, key):
        """Return the value associated with a key, only using the local dict."""

        # Return from local cache if found
        if key in self.toobig_dict:
            return self.toobig_dict[key]

        if key in self.local_value_by_key:
            return self.local_value_by_key[key]

        return None

    def get_now(self, key):
        """Return the non-local value associated with a key, even if blocked."""

        result = self.mc.get(key)
        if result is None:
            return None

        (value, lifetime) = result
        return value

    ######## Set methods

    def set(self, key, value, lifetime=None, pause=False):
        """Set a single value. Preserve a previously-defined lifetime (and reset
        the clock) if lifetime is None."""

        if key in self.toobig_dict:
            self.toobig_dict[key] = value
            return

        if (lifetime is None) and (key not in self.local_lifetime_by_key):
            try:
                (_, lifetime) = self.mc[key]
            except KeyError:
                pass

        self.set_local(key, value, lifetime)

        if not pause:
            self._flush_if_necessary()

        return True

    def __setitem__(self, key, value):
        """Enable dictionary syntax."""

        _ = self.set(key, value, lifetime=None)

    def set_multi(self, mydict, lifetime=None, pause=False):
        """Set multiple values at one time based on a dictionary. Preserve a
        previously-defined lifetime (and reset the clock) if lifetime is None.
        """

        # Separate keys into local, toobig, and non-local (in memcache)
        nonlocal_keys = set(mydict.keys())
        toobig_keys = set(self.toobig_dict.keys()) & nonlocal_keys
        nonlocal_keys -= toobig_keys

        local_keys = set(self.local_value_by_key.keys()) & nonlocal_keys
        nonlocal_keys -= local_keys

        # Retrieve lifetimes from cache if necessary
        if lifetime is None and nonlocal_keys:
            nonlocal_dict = self.mc.get_multi(nonlocal_keys)
            for (key, tuple) in nonlocal_dict:
                lifetime = tuple[1]
                self.local_lifetime_by_key[key] = lifetime

        # Save or update values in local cache
        for (key, value) in mydict.items():
            if key in toobig_keys:
                self.toobig_dict[key] = value
            else:
                self.set_local(key, value, lifetime)   # this resets the clock

        if not pause:
            self._flush_if_necessary()

        return []

    def set_local(self, key, value, lifetime=None):
        """Set or update a single value in the local cache. If lifetime is None,
        it preserves the lifetime of any value already in the local cache. The
        nonlocal cache is not checked."""

        # Deal with objects already identified as "too big". Once an item is
        # identified as too big, it will always reside in the internal
        # toobig_dict and should never expire.
        if key in self.toobig_dict:
            self.toobig_dict[key] = value
            return

        # If the local cache is empty, start the timer
        if len(self.local_value_by_key) == 0:
            self.flushtime = time.time() + self.localtime

        # Save the value
        self.local_value_by_key[key] = value

        # Determine the lifetime
        if lifetime is None:
            try:
                lifetime = self.local_lifetime_by_key[key]
            except KeyError:
                if self.lifetime:
                    lifetime = self.lifetime
                else:
                    lifetime = int(self.lifetime_func(value) + 0.999)

        # Remove an outdated key from the lifetime-to-keys dictionary
        try:
            prev_lifetime = self.local_lifetime_by_key[key]
            if prev_lifetime != lifetime:
                self.local_keys_by_lifetime[prev_lifetime].remove(key)
                if len(self.local_keys_by_lifetime[prev_lifetime]) == 0:
                    del self.local_keys_by_lifetime[prev_lifetime]
        except (KeyError, ValueError):
            pass

        # Insert the key into the lifetime-to-keys dictionary
        if lifetime not in self.local_keys_by_lifetime:
            self.local_keys_by_lifetime[lifetime] = [key]
        elif key not in self.local_keys_by_lifetime[lifetime]:
            self.local_keys_by_lifetime[lifetime].append(key)

        # Insert the key into the key-to-lifetime dictionary
        self.local_lifetime_by_key[key] = lifetime

    ######## Delete methods

    def delete(self, key):
        """Delete one key. Return True if it was deleted, False otherwise."""

        block_was_logged = False
        while self.is_blocked():
            if not block_was_logged and self.logger:
                self.logger.info(f'Process {self.pid} is blocked at delete() ' +
                                 f'on MemcacheCache [{self.port}]')
                block_was_logged = True
            time.sleep(0.5 * (1. + random.random()))  # A random short delay

        if block_was_logged and self.logger:
            self.logger.info(f'Process {self.pid} is unblocked at delete() ' +
                             f'on MemcacheCache [{self.port}]')

        status1 = self.mc.delete(key)
        status2 = self._delete_local(key)

        if key in self.permanent_values:
            del self.permanent_values[key]

        if key in self.toobig_dict:
            del self.toobig_dict[key]

        return status1 or status2

    def __delitem__(self, key):
        """Enable the "del" operator. Raise KeyError if the key is absent."""

        status = self.delete(key)
        if status:
            return

        raise KeyError(key)

    def delete_multi(self, keys):
        """Delete multiple items based on a list of keys. Keys not found in
        the cache are ignored. Returns True if all keys were deleted."""

        # Wait for block
        block_was_logged = False
        while self.is_blocked():
            if not block_was_logged and self.logger:
                self.logger.info(f'Process {self.pid} is blocked at ' +
                                 f'delete_multi() on ' +
                                 f'MemcacheCache [{self.port}]')
                block_was_logged = True
            time.sleep(0.5 * (1. + random.random()))  # A random short delay

        if block_was_logged and self.logger:
            self.logger.info(f'Process {self.pid} is unblocked at ' +
                             f'delete_multi() on MemcacheCache [{self.port}]')

        # Delete whatever we can from the nonlocal cache
        _ = self.mc.del_multi(keys)

        # Save the current length
        prev_len = len(self)

        # Delete whatever we can from the local cache and  permanent dictionary
        for key in keys:
            _ = self._del_local(key)

            if key in self.permanent_values:
                del self.permanent_values[key]

            if key in self.toobig_dict:
                del self.toobig_dict[key]

        count = len(self) - prev_len
        return (count == len(keys))

    def _delete_local(self, key):
        """Delete a single key from the local cache, if present. The nonlocal
        cache is not checked. Return True if deleted, False otherwise."""

        deleted = False
        if key in self.toobig_dict:
            del self.toobig_dict[key]
            deleted = True
 
        if key in self.local_lifetime_by_key:
            del self.local_value_by_key[key]
            deleted = True

            lifetime = self.local_lifetime_by_key[key]
            self.local_keys_by_lifetime[lifetime].remove(key)
            if len(self.local_keys_by_lifetime[lifetime]) == 0:
                del self.local_keys_by_lifetime[lifetime]

            del self.local_lifetime_by_key[key]

        return deleted

    def clear(self, block=False):
        """Clear all contents of the cache."""

        block_was_logged = False
        while self.is_blocked():
            if not block_was_logged and self.logger:
                self.logger.info(f'Process {self.pid} is blocked at clear() ' +
                                 f'on MemcacheCache [{self.port}]')
                block_was_logged = True
            time.sleep(0.5 * (1. + random.random()))  # A random short delay

        if block_was_logged and self.logger:
            self.logger.info(f'Process {self.pid} is unblocked at clear() ' +
                             f'on MemcacheCache [{self.port}]')

        # Clear the cache except for critical info
        self.block()
        clear_count = self.mc.get('$CLEAR_COUNT') + 1
        self.mc.flush_all()
        self.mc.set_multi({'$OK_PID': self.pid,
                           '$CLEAR_COUNT': clear_count}, time=0)

        self.local_value_by_key.clear()
        self.local_keys_by_lifetime.clear()
        self.local_lifetime_by_key.clear()
        self.permanent_values.clear()
        self.toobig_dict.clear()
        self.clear_count = clear_count

        if self.logger:
            self.logger.info(f'Process {self.pid} has set clear count to ' +
                             f'{self.clear_count} on ' +
                             f'MemcacheCache [{self.port}]')

        if block:
            if self.logger:
              self.logger.info(f'Process {self.pid} has completed clear() of ' +
                               f'MemcacheCache [{self.port}] ' +
                               f'but continues to block')

        else:
            self.mc.set('$OK_PID', 0, time=0)

            if self.logger:
              self.logger.info(f'Process {self.pid} has completed clear of ' +
                               f'MemcacheCache [{self.port}]')

    def replicate_clear(self, clear_count):
        """Clear the local cache if clear_count was incremented.

        Return True if cache was cleared; False otherwise.
        """

        if clear_count == self.clear_count: return False

        self.local_value_by_key.clear()
        self.local_keys_by_lifetime.clear()
        self.local_lifetime_by_key.clear()
        self.permanent_values.clear()
        self.toobig_dict.clear()
        self.clear_count = clear_count

        if self.logger:
          self.logger.info(f'Process {self.pid} has replicated clear of ' +
                           f'MemcacheCache [{self.port}]')
        return True

    def replicate_clear_if_necessary(self):
        """Clear the local cache only if MemCache was cleared."""

        clear_count = self.mc.get('$CLEAR_COUNT')
        self.replicate_clear(clear_count)

    def was_cleared(self):
        """Returns True if the cache has been cleared."""

        clear_count = self.mc.get('$CLEAR_COUNT')
        return clear_count > self.clear_count

    def _restore_permanent_to_cache(self):
        """Write every permanent value to the cache. This is triggered if any
        permanent value disappears from memcache. It ensures that permanent
        values are always in memcache."""

        # Update permanent values from cache; prepare to write remainder back
        local_dict = self.permanent_values.copy()
        for (key, pair) in self.permanent_values.items():
            pair = self.mc.get(key)
            if pair:
                self.permanent_values[key] = pair[0]
                del local_dict[key]

        # At this point local_dict contains all the permanent values currently
        # missing from the cache

        # Write the missing values into the local cache
        self.pause()
        try:
            for (key, value) in local_dict.items():
                self.set_local(key, value, lifetime=0)
        finally:
            self.resume()
            self.flush()

