#!/bin/bash
cd data
cat fluData* > allFluData.csv
echo -e "releaseDate,region,EW,lag,ili,wili" | cat - allFluData.csv > allFluData_withHeader.csv
