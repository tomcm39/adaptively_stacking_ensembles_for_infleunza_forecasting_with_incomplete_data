
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
LOG := fig2_logScoresFor20102011Training.log

fig2_logScoresFor20102011Training.pdf: fig2_logScoresFor20102011Training.py\
				       $(_5)/analysisData_preSeason/allEnsembleScores.csv
	$(PYTHON) $(PYTHON_OPTS) fig2_logScoresFor20102011Training.py
	$(call timeStamp,$(LOG),"fig2 created")

$(_5)/analysisData_preSeason/allEnsembleScores.csv:
	cd $(_5) && $(MAKE) 
