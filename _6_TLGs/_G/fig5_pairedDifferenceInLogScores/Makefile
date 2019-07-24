
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

LOG := fig5_pairedDifferencesOnLogScores.log


$(LOG): fig5_pairedDifferencesOnLogScores.pdf
	$(call timeStamp,$(LOG),"fig5 created")

fig5_pairedDifferencesOnLogScores.pdf: fig5_pairedDifferencesOnLogScores.py\
				       ../../_T/tab1_ensembleComparisons/tableData/deRslts.csv\
				       ../../_T/tab1_ensembleComparisons/tableData/dsRslts.csv
	$(PYTHON) $(PYTHON_OPTS) fig5_pairedDifferencesOnLogScores.py
	$(call timeStamp,$(LOG),"fig5 updated")

../../_T/tab1_ensembleComparisons/tableData/deRslts.csv:
	$(MAKE) -C ../../_T/tab1_ensembleComparisons

../../_T/tab1_ensembleComparisons/tableData/dsRslts.csv:
	$(MAKE) -C ../../_T/tab1_ensembleComparisons
