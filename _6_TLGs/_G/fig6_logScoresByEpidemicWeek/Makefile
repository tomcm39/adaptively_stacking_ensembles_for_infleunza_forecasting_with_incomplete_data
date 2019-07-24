
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

LOG := fig6_logScoresOverEpidemicWeeks.log

$(LOG): fig6_logScoresOverEpidemicWeeks.pdf\
	fig6_logScoresOverEpidemicWeeks_median.pdf
	$(call timeStamp,$(LOG),"fig6 created")

fig6_logScoresOverEpidemicWeeks.pdf : fig6_logScoresOverEpidemicWeeks.py
	$(PYTHON) $(PYTHON_OPTS) fig6_logScoresOverEpidemicWeeks.py
	$(call timeStamp,$(LOG),"fig6 updated")

fig6_logScoresOverEpidemicWeeks_median.pdf : fig6_logScoresOverEpidemicWeeks_median.py
	$(PYTHON) $(PYTHON_OPTS) fig6_logScoresOverEpidemicWeeks_median.py
	$(call timeStamp,$(LOG),"fig6 w/ median updated")
