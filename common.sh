statnett_table_datasets=(
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

function concat_csv() {
    local header_set=""
    for csv_path in "$@"; do
        if [[ -z "$header_set" ]]; then
            head -n 1 "$csv_path"
            header_set=1
        fi

        tail -n +2 "$csv_path"
    done
}
