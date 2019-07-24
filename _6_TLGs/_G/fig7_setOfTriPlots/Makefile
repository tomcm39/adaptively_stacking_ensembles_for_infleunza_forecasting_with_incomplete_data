
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

LOG := fig7_setOfTriplots.log

$(LOG): fig7_setOfTriplots.pdf
	$(call timeStamp,$(LOG),"fig7 created")

fig7_setOfTriplots.pdf: fig7_setOfTriplots.py
	$(PYTHON) $(PYTHON_OPTS) fig7_setOfTriplots.py
	$(call timeStamp,$(LOG),"fig7 updated")
