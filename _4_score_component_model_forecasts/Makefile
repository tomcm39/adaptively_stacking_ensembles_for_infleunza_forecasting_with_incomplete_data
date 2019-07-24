
#functions----------------------------
define timeStamp
	@echo $(2) "`date -u`" >> $(1)
endef
#-------------------------------------

#code options-------------------------
PYTHON = \python3
PYTHON_OPTS = -W ignore
#-------------------------------------

#folders------------------------------
_3 := ../_3_collect_and_process_individual_forecasts/aggregatedComponentForecasts
#-------------------------------------
.PHONY: createComponentModelList curlWiliBaselines
LOG := componentModelScores.log

FORECASTMODELS := $(wildcard $(_3)/*.csv.gz)
FORECASTSCORES := $(patsubst $(_3)/%.csv.gz,analysisData/scoringData_%.csv.gz,$(FORECASTMODELS)) 

componentModelScores.log: analysisData/allFSNLogScores.csv.gz
	$(call timeStamp,$(LOG),"allFSNLogScores.csv.gz created")

analysisData/allFSNLogScores.csv.gz : $(FORECASTSCORES) computeLogScoresForAllComponentForecasts.py \
				      wiliBaselineDataByRegionAndYear/wILI_Baseline.csv
	$(PYTHON) $(PYTHON_OPTS) combineAndPivotDataModelPerColumn.py
	cd analysisData; gzip allFSNLogScores.csv
	$(call timeStamp,$(LOG),"combining forecast scores")

$(FORECASTSCORES): $(FORECASTMODELS) \
		   ../_3_collect_and_process_individual_forecasts/allPossibleEpidemicWeeks.csv \
		   ../_2_processRawILIdata/analysisData/allFluData__releaseDate_location_EW_lag_ili_wili_year_week_modelWeek_calendarEW_Season.csv\
		   componentModelForecasts.csv
	\mkdir -p analysisData
	$(PYTHON) $(PYTHON_OPTS) computeLogScoresForAllComponentForecasts.py $<
	$(call timeStamp,$(LOG),scoring component models)

componentModelForecasts.csv : fillInFSNForecastModels.py
	$(PYTHON) $(PYTHON_OPTS) fillInFSNForecastModels.py
	$(call timeStamp,$(LOG),"created list of component models")

createComponentModelList:
	$(PYTHON) $(PYTHON_OPTS) fillInFSNForecastModels.py
	$(call timeStamp,$(LOG),"created list of component models")

wiliBaselineDataByRegionAndYear/wILI_Baseline.csv: transposeBaselineLevels.py
	curlWiliBaselines

curlWiliBaselines:
	\mkdir -p wiliBaselineDataByRegionAndYear
	curl https://raw.githubusercontent.com/cdcepi/FluSight-forecasts/master/wILI_Baseline.csv | sed s/[,]$$// | python3 transposeBaselineLevels.py
	$(call timeStamp,$(LOG),"created baseline model")

createFolder:
	\mkdir -p analysisData
	\mkdir -p wiliBaselineDataByRegionAndYear
