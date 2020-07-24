#!/bin/bash
echo "Clean up previous coverage record"
coverage erase
count=1
numOfModes=2
targetFile="pdsfile.py"
while [ $count -le $numOfModes ]
do
    echo "Run mode $count"
    coverage run --parallel-mode -m pytest tests/ --mode $count
    count=`expr $count + 1`
done
echo "Combine results from all modes"
coverage combine
echo "Report coverage on pdsfile.py"
coverage report |grep $targetFile
echo "Generate html"
coverage html
