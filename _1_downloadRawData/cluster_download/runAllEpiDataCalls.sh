#!/bin/bash

cat ../queueOfYearsAndRegions2download.csv | while read line
do
    echo "$line"
    bsub -env "$line" < epiCall.sh
    sleep 4
done




