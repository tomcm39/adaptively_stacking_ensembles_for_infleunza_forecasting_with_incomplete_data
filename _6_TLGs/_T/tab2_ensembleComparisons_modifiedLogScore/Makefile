
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

LOG := tab2_ensembleComparisons_modifiedLogScore.log

$(LOG): tableData/deRslts.csv tableData/dsRslts.csv
	$(call timeStamp,$(LOG),"comparisons made")

tableData/deRslts.csv:
	\mkdir -p tableData 
	Rscript --vanilla ensembleComparisons__Adaptive_vs_Equal.R
	$(call timeStamp,$(LOG),"adaptive vs equal dataset created")

tableData/dsRslts.csv:
	\mkdir -p tableData 
	Rscript --vanilla ensembleComparisons__Adaptive_vs_Static.R
	$(call timeStamp,$(LOG),"adaptive vs static dataset created")
