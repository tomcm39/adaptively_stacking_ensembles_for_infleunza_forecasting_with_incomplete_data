
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
_5 := ../../../_5_compute_and_score__ensembles
#-------------------------------------
.PHONY:
TRIPLOTS := $(shell bash listTriplots.sh)
LOG := fig3_triPlot.log

$(LOG): $(TRIPLOTS)
$(TRIPLOTS): fig3_triPlot.py\
	     $(_5)/analysisData/allEnsembleWeights.csv
	SEASON=`echo $@ | grep -o "[0-9]\+_[0-9]\+" | tr "_" "/"` &&\
	echo plotting season $$SEASON &&\
	$(PYTHON) $(PYTHON_OPTS) fig3_triPlot.py --season $$SEASON
	$(call timeStamp,$(LOG),"fig3 created")

$(_5)/analysisData/allEnsembleWeights.csv:
	cd $(_5) && $(MAKE)
