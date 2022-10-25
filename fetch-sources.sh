#!/usr/bin/bash

# load common helpers
source common.sh

# setup variables
OUTPUT_DIR=raw
BEGIN_YEAR=1970
END_YEAR=$(date +"%Y")
STATNETT_RESTAPI_ENDPOINT="https://driftsdata.statnett.no/restapi"
STATNETT_WEB_DOWNLOAD_ENDPOINT="$STATNETT_RESTAPI_ENDPOINT/Download"

# setup output directory
mkdir -p "$OUTPUT_DIR"

function fetch_statnett_web_download() {
	for dataset_name in ${statnett_table_datasets[@]}; do
		echo "downloading dataset $dataset_name"
		mkdir -p "$OUTPUT_DIR/$dataset_name"
		for year in $(seq $BEGIN_YEAR $END_YEAR); do
			echo "downloading year $year"
			local dataset_url="$STATNETT_WEB_DOWNLOAD_ENDPOINT/$dataset_name/$year"
			curl -s -o "$OUTPUT_DIR/$dataset_name/$dataset_name"_"$year.xls" "$dataset_url" &
		done
		echo "waiting for all $dataset_name downloads to finish"
		wait
	done

	echo "removing empty datasets"
	grep -F -r -l "\"success\":false" raw | xargs rm
	grep -F -r -l "<font color=red face=Arial size=12px>missing data</font>" "$OUTPUT_DIR" | xargs rm
	find raw -type f -size 0 -exec rm {} \;
}

# main
fetch_statnett_web_download
