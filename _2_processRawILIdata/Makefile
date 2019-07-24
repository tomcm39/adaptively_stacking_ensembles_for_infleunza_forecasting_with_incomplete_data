BASEFILE := ./analysisData/allFluData__releaseDate_location_EW_lag_ili_wili_year_week_modelWeek

$(BASEFILE)_calendarEW_Season.csv: $(BASEFILE)_calendarEW.csv
	python3 addInSeason.py

$(BASEFILE)_calendarEW.csv: $(BASEFILE).csv
	python3 addInCalendarEpidemicWeek.py

$(BASEFILE).csv: ../_1_downloadRawData/data/allFluData_withHeader.csv
	mkdir -p analysisData
	Rscript --vanilla processRawFluDataIntoAnalysisDataset.R
