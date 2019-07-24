
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
LOG := fig10_logScoresForAllEnsemble.log

fig10_logScoresForAllEnsemble.pdf: fig10_logScoresForAllEnsemble.py\
				   data.log
	$(PYTHON) $(PYTHON_OPTS) fig10_logScoresForAllEnsemble.py
	$(call timeStamp,$(LOG),"fig10 created")

data.log: computeDataForPlot.py
	\mkdir -p plotData
	$(PYTHON) $(PYTHON_OPTS) computeDataForPlot.py
	$(call timeStamp,"data.log","fig10 data generated")
