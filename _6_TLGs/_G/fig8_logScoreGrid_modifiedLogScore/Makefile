
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

LOG := fig8_logScoreGrid_modifiedLogScore.log

$(LOG): fig8_logScoreGrid_modifiedLogScore.pdf
	$(call timeStamp,$(LOG),"fig8 created")

fig8_logScoreGrid_modifiedLogScore.pdf: fig8_logScoreGrid_modifiedLogScore.py\
					data.log
	$(PYTHON) $(PYTHON_OPTS) fig8_logScoreGrid_modifiedLogScore.py
	$(call timeStamp,$(LOG),"fig8 updated")

data.log: computeDataForPlot.py
	\mkdir -p plotData
	$(PYTHON) $(PYTHON_OPTS) computeDataForPlot.py
	$(call timeStamp,"data.log","plot data updated")


