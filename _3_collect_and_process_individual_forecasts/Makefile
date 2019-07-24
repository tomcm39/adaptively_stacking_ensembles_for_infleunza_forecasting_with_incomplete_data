#!/bin/bash

FORECASTFILES := $(wildcard aggregatedComponentForecasts/*.csv)
ZFORECASTFILES := $(wildcard aggregatedComponentForecasts/*.csv.gz)
SEPFORECASTS := $(wildcard separateComponentModelForecasts/*/*.csv)

.PHONY: createAllEpiWeeks creatDir

aggregated.log: aggregateForecastsByModel.py addScoringWeeks.py processRegionAndNoneBins.py $(SEPFORECASTS) $(FORECASTFILES) $(ZFORECASTFILES)
	@echo "aggregating separate component model forecasts"
	python3 aggregateForecastsByModel.py
	@echo "aggregateForecasts = `date -u`" >> aggregated.log
	python3 addScoringWeeks.py
	@echo "addScoringWeeks = `date -u`" >> aggregated.log
	python3 processRegionAndNoneBins.py
	@echo "processRegionAndNoneBins = `date -u`" >> aggregated.log	
	cd aggregatedComponentForecasts; gzip *.csv
	@echo "zipped csv forecasts" % "= `date -u`" >> aggregated.log

createAllEpiWeeks:
	python3 createListOfAllPossibleEpidemicWeeks.py
	@echo "allPossibleEpidemicWeeks = `date -u`" >> aggregated.log

creatDir:
	@mkdir -p aggregatedComponentForecasts

clean:
	rm ./aggregatedComponentForecasts/*
	rm aggregated.log
