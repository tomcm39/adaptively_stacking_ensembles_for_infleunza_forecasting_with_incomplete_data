
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
#-------------------------------------
.PHONY:

LOG := fig9_pairedDifferenceInLogScores_modifiedLogScore.log

$(LOG): fig9_pairedDifferenceInLogScores_modifiedLogScore.pdf
	$(call timeStamp,$(LOG),"fig9 created")

fig9_pairedDifferenceInLogScores_modifiedLogScore.pdf: fig9_pairedDifferenceInLogScores_modifiedLogScore.py\
						       data.log
	$(PYTHON) $(PYTHON_OPTS) fig9_pairedDifferenceInLogScores_modifiedLogScore.py 
	$(call timeStamp,$(LOG),"fig9 updated")

data.log: 
	cd ../../_T/tab2_ensembleComparisons_modifiedLogScore && $(MAKE)  
	$(call timeStamp,"data.log","fig9 updated")
