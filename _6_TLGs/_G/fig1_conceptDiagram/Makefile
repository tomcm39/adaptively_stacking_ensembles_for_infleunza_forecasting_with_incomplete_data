
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

LOG := fig1_conceptDiagram.log

fig1_conceptDiagram.pdf: plotConceptDiagram.py
	$(PYTHON) $(PYTHON_OPTS) plotConceptDiagram.py
