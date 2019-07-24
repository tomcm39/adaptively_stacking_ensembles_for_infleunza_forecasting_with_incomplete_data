
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
_4 := ../_4_score_component_model_forecasts
#-------------------------------------
.PHONY: createComponentModelList curlWiliBaselines
LOG := ensembleScores.log

EWSCORES  := analysisData/ensembleScores__equalscore.csv
EWWEIGHTS := analysisData/ensembleWeights__equalweight.csv

PRIORSTART := 0
PRIOREND   := 1.01
PRIORSTEP  := 0.01

STSCORES  := $(shell seq $(PRIORSTART) $(PRIORSTEP) $(PRIOREND) | xargs printf "analysisData/ensembleScores__staticscore_%6.4f.csv ")
STWEIGHTS := $(shell seq $(PRIORSTART) $(PRIORSTEP) $(PRIOREND) | xargs printf "analysisData/ensembleWeights__staticweight_%6.4f.csv ")

ADSCORES  := $(shell seq $(PRIORSTART) $(PRIORSTEP) $(PRIOREND) | xargs printf "analysisData/ensembleScores__adaptscore_%6.4f.csv ")
ADWEIGHTS := $(shell seq $(PRIORSTART) $(PRIORSTEP) $(PRIOREND) | xargs printf "analysisData/ensembleWeights__adaptweight_%6.4f.csv ")

PREADSCORES  := $(shell seq $(PRIORSTART) $(PRIORSTEP) $(PRIOREND) | xargs printf "analysisData_preSeason/ensembleScores__adaptscore_%6.4f.csv ")
PREADWEIGHTS := $(shell seq $(PRIORSTART) $(PRIORSTEP) $(PRIOREND) | xargs printf "analysisData_preSeason/ensembleWeights__adaptweight_%6.4f.csv ")

ensembleScores.log : analysisData/allEnsembleWeights.csv analysisData/allEnsembleScores.csv analysisData_preSeason/allEnsembleScores.csv
	$(call timeStamp,$(LOG),"run complete")

analysisData/allEnsembleScores.csv: $(EWSCORES) $(STSCORES) $(ADSCORES) 
	\mkdir -p analysisData
	$(PYTHON) $(PYTHON_OPTS) combineEnsembleScores.py --preSeason 0
	$(call timeStamp,$(LOG),"combined all ensemble scores")

analysisData/allEnsembleWeights.csv: $(EWWEIGHTS) $(STWEIGHTS) $(ADWEIGHTS)
	\mkdir -p analysisData
	$(PYTHON) $(PYTHON_OPTS) combineEnsembleWeights.py
	$(call timeStamp,$(LOG),"combined all ensemble weights")

analysisData_preSeason/allEnsembleScores.csv: $(PREADSCORES)
	\mkdir -p analysisData_preSeason
	$(PYTHON) $(PYTHON_OPTS) combineEnsembleScores.py --preSeason 1
	$(call timeStamp,$(LOG),"combined all 2010/2011 ensemble weights")

$(EWSCORES) $(EWWEIGHTS): $(_4)/analysisData/allFSNLogScores.csv.gz
	$(PYTHON) $(PYTHON_OPTS) process_EW.py
	@echo "equal weight ensembles assigned a prior = -2"
	$(call timeStamp,$(LOG),"produce EW ensemble data")

analysisData/ensembleWeights__staticweight_%.csv analysisData/ensembleScores__staticscore_%.csv: $(_4)/analysisData/allFSNLogScores.csv.gz listOfPriors.txt
	PRIOR := $(shell echo $@ | grep -o '[0-9].[0-9]\+')
	$(PYTHON) $(PYTHON_OPTS) process_static.py $(PRIOR)
	$(call timeStamp,$(LOG),"produce static ensemble data")

analysisData/ensembleWeights__adaptweight_%.csv analysisData/ensembleScores__adaptscore_%.csv: $(_4)/analysisData/allFSNLogScores.csv.gz listOfPriors.txt
	PRIOR := $(shell echo $@ | grep -o '[0-9].[0-9]\+')
	$(PYTHON) $(PYTHON_OPTS) process_adaptive.py --preSeason 0 --prior $(PRIOR)
	$(call timeStamp,$(LOG),"produce adaptive ensemble data")

analysisData_preSeason/ensembleWeights__adaptweight_%.csv analysisData_preSeason/ensembleScores__adaptscore_%.csv: $(_4)/analysisData/allFSNLogScores.csv.gz listOfPriors.txt
	PRIOR := $(shell echo $@ | grep -o '[0-9].[0-9]\+')
	$(PYTHON) $(PYTHON_OPTS) process_adaptive.py --preSeason 1 --prior $(PRIOR)
	$(call timeStamp,$(LOG),"produce adaptive ensemble data for 2010/2011 season")
