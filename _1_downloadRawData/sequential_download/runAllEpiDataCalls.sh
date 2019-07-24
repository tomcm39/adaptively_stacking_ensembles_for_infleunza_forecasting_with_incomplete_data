#!/bin/bash

cat ../queueOfYearsAndRegions2download.csv | while read line
do
    echo $line
    line=$(python stripExtra.py $line)
    echo $line
    bash epiCall.sh $line 
    sleep 4
done
