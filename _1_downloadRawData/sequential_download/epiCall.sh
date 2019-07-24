#!/bin/bash

cd ..
echo Year = $1
echo Region = $2
echo "Starting"
python3 downloadRawData_inputYearAndRegion.py $1 $2
echo "finished"
