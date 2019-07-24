Transform raw ILI data into analysis dataset
======================

## Brief Description

This folder transforms the raw ILI data, stored in \_1\_downloadRawData/data/ into an analysis dataset.
Running this makefile by executing `make` adds useful columns to the raw ILI data needed in further analysis.
An example of the final analysisDataset is shown below.

## Example of Final AnalysisData (./analysisData/allFluData\*calendarEW_Season.csv)
releaseDate  |  region  |  EW      |  lag  |  ili      |  wili     |  year  |  week  |  modelWeek  |  calendarEW  |  Season
-------------|----------|----------|-------|-----------|-----------|--------|--------|-------------|--------------|-----------
2010-01-15   |  HHS10   |  201001  |  0    |  1.27325  |  1.11231  |  2010  |  1     |  53         |  201002      |  2009/2010
2010-01-15   |  HHS1    |  201001  |  0    |  0.77017  |  0.76613  |  2010  |  1     |  53         |  201002      |  2009/2010
2010-01-15   |  HHS2    |  201001  |  0    |  2.27247  |  1.26799  |  2010  |  1     |  53         |  201002      |  2009/2010
2010-01-15   |  HHS3    |  201001  |  0    |  2.1217   |  1.7909   |  2010  |  1     |  53         |  201002      |  2009/2010
2010-01-15   |  HHS4    |  201001  |  0    |  2.16424  |  1.85445  |  2010  |  1     |  53         |  201002      |  2009/2010
2010-01-15   |  HHS5    |  201001  |  0    |  1.47977  |  1.28161  |  2010  |  1     |  53         |  201002      |  2009/2010
2010-01-15   |  HHS6    |  201001  |  0    |  2.4048   |  2.2529   |  2010  |  1     |  53         |  201002      |  2009/2010
2010-01-15   |  HHS7    |  201001  |  0    |  1.7066   |  1.6796   |  2010  |  1     |  53         |  201002      |  2009/2010
2010-01-15   |  HHS8    |  201001  |  0    |  0.70489  |  0.62674  |  2010  |  1     |  53         |  201002      |  2009/2010
