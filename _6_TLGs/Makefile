
SUBDIRS := $(wildcard */)
build: $(SUBDIRS)
$(SUBDIRS):
	$(MAKE) -C $@
.PHONY: all $(SUBDIRS)

