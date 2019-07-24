
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
_1 := _1_downloadRawData
_2 := _2_processRawILIdata
_3 := _3_collect_and_process_individual_forecasts
_4 := _4_score_component_model_forecasts
_5 := _5_compute_and_score__ensembles
_6 := _6_TLGs
_7 := _7_manuscript
#-------------------------------------

LOG := adaptively_stacking_ensembles_for_infleunza_forecasting_with_incomplete_data.log
SUBDIRS := $(wildcard */)

build: $(SUBDIRS)
$(SUBDIRS):
	$(MAKE) -C $@
.PHONY: all $(SUBDIRS)
