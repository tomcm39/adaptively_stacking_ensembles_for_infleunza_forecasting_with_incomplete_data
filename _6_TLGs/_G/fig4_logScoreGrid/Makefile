
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

LOG := fig4_logScoreGrid.log

$(LOG) : fig4_logScoreGrid.pdf
	$(call timeStamp,$(LOG),"fig4 created")

fig4_logScoreGrid.pdf: fig4_logScoreGrid.py plotData.log
	$(PYTHON) $(PYTHON_OPTS) fig4_logScoreGrid.py
	$(call timeStamp,$(LOG),"fig4 updated")

plotData.log:
	\mkdir -p plotData
	$(PYTHON) $(PYTHON_OPTS) computeDataForPlot.py
	$(call timeStamp,plotData.log,"plot data processed")
