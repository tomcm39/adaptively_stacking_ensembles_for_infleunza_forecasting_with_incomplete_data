
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
_7 := _7_manuscript
#-------------------------------------

LOG := adaptively_stacking_ensembles_for_infleunza_forecasting_with_incomplete_data.log

$(LOG): $(_7)/main.pdf
	$(call timeStamp,$(LOG),"updated manuscript")

$(_7)/main.pdf:
	cd $(_7) && $(MAKE)
