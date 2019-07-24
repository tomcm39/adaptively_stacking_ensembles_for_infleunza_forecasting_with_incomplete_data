Aggregate component model forecasts from the FluSightNetwork(FSN)
===============

## Brief description

This step in our analysis pipeline takes all the component forecasts from the FSN's [git repo](https://github.com/FluSightNetwork/cdc-flusight-ensemble) and creates a single csv file per component model forecast. 
Raw component model forecast data is located in the `./cdc-flusight-ensemble/model-forecasts/component-models/` folder of the git repo, and should be downloaded to `./separateComponentModelForecasts/` .
Aggregated and processed data is sent to `/aggregatedComponentForecasts/` and gzipped.

Among many processing steps, a variable called scoring week is added to all forecast datasets. 
A scoring week is defined as the Epiweek (year and week) to evaluate a forecast against.
For example: the 1 week ahead forecast for Epiweek 201304 can be compared against the wili value on Epiweek 201305.
We call 201305 the scoring week.

## Example of Data (./aggregatedComponentForecasts/ReichLab_kdeForecasts.csv)

model         |  year  |  EW  |  EWNum   |  season     |  region       |  target        |  bin0  |  bin1  |  prob                  |  scoringWeek
--------------|--------|------|----------|-------------|---------------|----------------|--------|--------|------------------------|-------------
ReichLab-KDE  |  2016  |  47  |  201647  |  2016/2017  |  US National  |  Season onset  |  40    |  41    |  0.014663              |  201739.0
ReichLab-KDE  |  2016  |  47  |  201647  |  2016/2017  |  US National  |  Season onset  |  41    |  42    |  0.012394              |  201739.0
ReichLab-KDE  |  2016  |  47  |  201647  |  2016/2017  |  US National  |  Season onset  |  42    |  43    |  0.005586              |  201739.0
ReichLab-KDE  |  2016  |  47  |  201647  |  2016/2017  |  US National  |  Season onset  |  43    |  44    |  0.004262              |  201739.0
ReichLab-KDE  |  2016  |  47  |  201647  |  2016/2017  |  US National  |  Season onset  |  44    |  45    |  0.015041999999999996  |  201739.0
ReichLab-KDE  |  2016  |  47  |  201647  |  2016/2017  |  US National  |  Season onset  |  45    |  46    |  0.027051              |  201739.0
ReichLab-KDE  |  2016  |  47  |  201647  |  2016/2017  |  US National  |  Season onset  |  46    |  47    |  0.045679              |  201739.0
ReichLab-KDE  |  2016  |  47  |  201647  |  2016/2017  |  US National  |  Season onset  |  47    |  48    |  0.066482              |  201739.0
ReichLab-KDE  |  2016  |  47  |  201647  |  2016/2017  |  US National  |  Season onset  |  48    |  49    |  0.08302899999999999   |  201739.0
