#!/bin/bash
echo "Clean up previous coverage record"
coverage erase
count=1
numOfModes=2

while [ $count -le $numOfModes ]
do
    echo "Run mode $count"
    # Run tests under tests/ and rules/
    coverage run --parallel-mode -m pytest tests/ rules/*.py --mode $count
    count=`expr $count + 1`
done
echo "Combine results from all modes"
coverage combine
echo "Generate html"
coverage html
echo "Report coverage"
coverage report
