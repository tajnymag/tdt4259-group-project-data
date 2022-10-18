#!/usr/bin/bash

# setup variables
OUTPUT_DIR=raw
BEGIN_YEAR=1970
END_YEAR=$(date +"%Y")
STATNETT_RESTAPI_ENDPOINT="https://driftsdata.statnett.no/restapi"
STATNETT_WEB_DOWNLOAD_ENDPOINT="$STATNETT_RESTAPI_ENDPOINT/Download"

# setup output directory
mkdir -p "$OUTPUT_DIR"

statnett_web_download_datasets=(
	"productionconsumption"
	"physicalflow"
	"primaryreservesday"
	"primaryreservesdaytwo"
	"primaryreservesweek"
	"secondaryreserves"
	"rkomdata"
	"rkom"
)

statnett_json_datasets=(
	"Physicalflow/GetData"
	"ProductionConsumption/GetData"
	"ProductionConsumption/GetLatestDetailedOverview"
	"Reserves/PrimaryReservesPerDay"
	"Reserves/PrimaryReservesPerWeek"
	"Reserves/SecondaryReservesPerWeek"
	"Frequency/ByMinute"
	"Frequency/BySecond"
	"ElspotSeparatorLine/LastChanges"
	"ElspotSeparatorLine/AsPng"
	"ElspotSeparatorLine/AsPng/"
	"ElspotPowerSituation/LastChanges"
	"ElspotPowerSituation/GetPowerSituations"
	"PhysicalFlowMap/GetFlowMap"
	"PhysicalFlowMap/GetFlow"
	"Reservoir/LastWeekData/3"
	"Reservoir"
	"Reservoir/NveProxy"
	"Rkom/Year/2012"
	"Rkom/MetaData"
	"Systemprice"
	"Translator/Translations"
	"download"
	"Keyfigures"
)

function fetch_statnett_web_download() {
	for dataset_name in ${statnett_web_download_datasets[@]}; do
		echo "downloading dataset $dataset_name"
		mkdir -p "$OUTPUT_DIR/$dataset_name"
		for year in $(seq $BEGIN_YEAR $END_YEAR); do
			echo "downloading year $year"
			local dataset_url="$STATNETT_WEB_DOWNLOAD_ENDPOINT/$dataset_name/$year"
			curl -s -o "$OUTPUT_DIR/$dataset_name/$dataset_name"_"$year.xls" "$dataset_url"
		done
	done

	echo "removing empty datasets"
	grep -F -r -l "\"success\":false" raw | xargs rm
	grep -F -r -l "<font color=red face=Arial size=12px>missing data</font>" "$OUTPUT_DIR" | xargs rm
	find raw -type f -size 0 -exec rm {} \;
}

# main
fetch_statnett_web_download