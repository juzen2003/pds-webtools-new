#! /bin/zsh
################################################################################
# Synchronize one volume set from one pdsdata drive to another.
#
# Usage:
#   pdsdata-sync <old> <new> <volset> [--dry-run]
#
# Syncs the specified volume set <volset> from the drive /Volumes/pdsdata-<old>
# to the drive /Volumes/pdsdata-<new>. Append "--dry-run" for a test dry run.
#
# Example:
#   pdsdata-sync admin raid45 VGx_9xxx
# copies all files relevant to the volume set "VGx_9xxx" from the drive
# pdsdata-admin to the drive pdsdata-raid45.
################################################################################

for voltype in metadata previews calibrated diagrams volumes _infoshelf-volumes _infoshelf-archives-volumes _linkshelf-volumes _volinfo
do
  if [ -d /Volumes/pdsdata-$1/holdings/$voltype/$3 ]; then
    echo "\n\n**** holdings/archives-$voltype/$3 ****"
    rsync -av /Volumes/pdsdata-$1/holdings/archives-$voltype/$3/ \
              /Volumes/pdsdata-$2/holdings/archives-$voltype/$3/ $4

    echo "\n\n**** holdings/checksums-$voltype/$3 ****"
    rsync -av /Volumes/pdsdata-$1/holdings/checksums-$voltype/$3/ \
              /Volumes/pdsdata-$2/holdings/checksums-$voltype/$3/ $4

    echo "\n\n**** holdings/checksums-archives-$voltype/$3_*md5.txt ****"
    rsync -av --include="$3_md5.txt" --include="$3_${voltype}_md5.txt" \
              --exclude="*" \
              /Volumes/pdsdata-$1/holdings/checksums-archives-$voltype/ \
              /Volumes/pdsdata-$2/holdings/checksums-archives-$voltype/ $4

    echo "\n\n**** shelves/info/$voltype/$3 ****"
    rsync -av /Volumes/pdsdata-$1/shelves/info/$voltype/$3/ \
              /Volumes/pdsdata-$2/shelves/info/$voltype/$3/ $4

    echo "\n\n**** shelves/info/archives-$voltype/$3_info.py ****"
    rsync -av --include="$3_info.py" --include="$3_info.pickle" \
              --exclude="*" \
              /Volumes/pdsdata-$1/shelves/info/archives-$voltype/ \
              /Volumes/pdsdata-$2/shelves/info/archives-$voltype/ $4

    if [ -d /Volumes/pdsdata-$1/shelves/links/$voltype ]; then
      echo "\n\n**** shelves/info/links/$voltype/$3 ****"
      rsync -av /Volumes/pdsdata-$1/shelves/links/$voltype/$3/ \
                /Volumes/pdsdata-$2/shelves/links/$voltype/$3/ $4
    fi

    if [ -d /Volumes/pdsdata-$1/shelves/index/$voltype ]; then
      echo "\n\n**** shelves/info/index/$voltype/$3 ****"
      rsync -av /Volumes/pdsdata-$1/shelves/index/$voltype/$3/ \
                /Volumes/pdsdata-$2/shelves/index/$voltype/$3/ $4
    fi

    echo "\n\n**** holdings/$voltype/$3 ****"
    rsync -av /Volumes/pdsdata-$1/holdings/$voltype/$3/ \
              /Volumes/pdsdata-$2/holdings/$voltype/$3/ $4
  fi
done

################################################################################

################################################################################

