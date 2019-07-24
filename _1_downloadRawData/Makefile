
./data/allFluData_withHeader.csv: ./data/allFluData.csv
	echo "releaseDate,region,EW,lag,ili,wili" | cat - ./data/allFluData.csv > ./data/allFluData_withHeader.csv
	@echo "add header to flu data"

RAWDATA := $(wildcard ./data/fluData*)
./data/allFluData.csv: $(RAWDATA) 
	cat ./data/fluData* > ./data/allFluData.csv

downloadDataOnLocal: createDownloadQueue
	mkdir -p data
	cd sequential_download; bash runAllEpiDataCalls.sh

downloadDataOnCluster: createDownloadQueue
	mkdir -p data
	cd cluster_download; bash runAllEpiDataCalls.sh

createDownloadQueue:
	python3 create_queue_to_download_years_and_regions_of_ili_data.py
