# TDT4259 Group Project
Nordic power grid flow

## Sources

* https://driftsdata.statnett.no/Web/Download/
* https://driftsdata.statnett.no/restapi/
    * not used yet

## Data groups

### Power flow

Shows the power flow from and into Norway's power grid.

#### Variables (2019-)

| Variable | Unit | Type | Description |
| -------- | ---- | ---- | ----------- |
| Time(Local) | %m.%d.%y %H:%M %z | string | Date and time of the measurement |
| Import | MWh | float | Import into the whole norwegian power grid |
| Export | MWh | float | Export out of the whole norwegian power grid |
| Flow from NO | MWh | float | Flow from the norwegian power grid |

### Production and consumption

Shows the production and consumption of energy in all Norway.

#### Variables (2001-)

| Variable | Unit | Type | Description |
| -------- | ---- | ---- | ----------- |
| Time(Local) | %m.%d.%y %H:%M %z | string | Date and time of the measurement |
| Production | MWh | float | Production of energy in all Norway |
| Consumption | MWh | float | Consumption of energy in all Norway |

### Primary reserves

Shows the amount and pricing of primary reserves in the grid. **FCR** stands for **F**requency **C**ontrol **R**eserves. It can be coupled with either **N** or **D** postfix. **N** stands for *normal operation* and **D** stands for *disturbances*.

primaryreserves{day,two} should be merged

primaryreservesweek is basically agregated primaryreserves{day,two}

#### Variables (2013-)

| Variable | Unit | Type | Description |
|----------|------|------|-------------|
| Time(Local) | %m.%d.%y %H:%M %z | string | Date and time of the measurement |
| Hournumber | hour | integer | Hour of the day, same as in `Time(Local) + 1` |
| Area | - | NOK1, NOK2, NOK3, NOK4, NOK5 | Area of the measurement |
| FCR-N Price NOK/MWh | NOK/MWh| integer | Price for frequency control reserve per MWh|
| FCR-N Price EUR/MWh | EUR/MWh| integer | Price for frequency control reserve per MWh|
| FCR-N Volume MWh | MWh| integer | Volume of frequency control reserve |
| FCR-D Price EUR/MWh | EUR/MWh| integer | Price for frequency control reserve per MWh|
| FCR-D Volume MWh | MWh| integer | Volume of frequency control reserve |

### Secondary reserves

Shows the amount and pricing of secondary reserves in the grid. Also called **F**requency **C**ontrol **R**eserves.

secondaryreserves is similar to primaryreservesweek but for, wait for it, secondary reserves

#### Variables (2012-)

| Variable | Unit | Type | Description |
| -------- | ---- | ---- | ----------- |
| Year | year | integer | Year of the measurement |
| Week | week | integer | Week of the year of the measurement |
| Hour | hour | integer | Hour of the day of the measurement |
| Workday FRR-A Up Volume | MWh | integer | Volume of frequency restoration reserves for workdays |
| Workday FRR-A Up Price | NOK/MWh | integer | Price of frequency restoration reserves for workdays |
| Workday FRR-A Down Volume | MWh | integer | Volume of frequency restoration reserves for workdays |
| Workday FRR-A Down Price | NOK/MWh | integer | Price of frequency restoration reserves for workdays |
| Weekend FRR-A Up Volume | MWh | integer | Volume of frequency restoration reserves for weekends |
| Weekend FRR-A UP Price | NOK/MWh | integer | Price of frequency restoration reserves for weekends |
| Weekend FRR-A Down Volume | MWh | integer | Volume of frequency restoration reserves for weekends |
| Weekend FRR-A Down Price | NOK/MWh | integer | Price of frequency restoration reserves for weekends |

### RKOM

Shows data about the regulator power market. Each week there's a bidding process where the grid operators bid for the right to regulate the grid. Thus dataset contains information about week + price + hour of the day for MWh of energy in certain area.

Until 2014, Statnett released RKOM data divided into 3 areas. Since 2014, they've released it divided into 5 areas which are agreggated, unfortunately almost randomly, each year differently.

rkom and rkomdata is the same thing, but rkomdata is more is more detailed and starts at 2014

#### Variables (2004-2014)

| Variable | Unit | Type | Description |
| -------- | ---- | ---- | ----------- |
| Year | year | integer | Year of the measurement |
| Week | week | integer | Week of the year of the measurement |
| NOA-Price | NOK/MWh | integer | Price for MWh in NOA |
| NOA-Prod | MWh | integer | Production in NOA |
| NOA-Cons | MWh | integer | Consumption in NOA |
| NOB-Price | NOK/MWh | integer | Price for MWh in NOB |
| NOB-Prod | MWh | integer | Production in NOB |
| NOB-Cons | MWh | integer | Consumption in NOB |
| NOC-Price | NOK/MWh | integer | Price for MWh in NOC |
| NOC-Prod | MWh | integer | Production in NOC |
| NOC-Cons | MWh | integer | Consumption in NOC |

#### Variables (2014-)

| Variable | Unit | Type | Description |
| -------- | ---- | ---- | ----------- |
| Year | year | integer | Year of the measurement |
| Week | week | integer | Week of the year of the measurement |
| Areas | - | NOK1, NOK2, NOK3, NOK4, NOK5 | Pricing areas for the bidding |
| Direction | - | Up, Down | **No idea what it is** |
| RKOM-H Volume Weekday | MWh | integer | Volume of primary reserves for workdays |
| RKOM-H Price Weekday | NOK/MWh | integer | Price of primary reserves for workdays |
| RKOM-H Volume Weekend | MWh | integer | Volume of primary reserves for weekends |
| RKOM-H Price Weekend | NOK/MWh | integer | Price of primary reserves for weekends |
| RKOM-B Volume Weekday | MWh | integer | Volume of secondary reserves for workdays |
| RKOM-B Price Weekday | NOK/MWh | integer | Price of secondary reserves for workdays |
| RKOM-B Volume Weekend | MWh | integer | Volume of secondary reserves for weekends |
| RKOM-B Price Weekend | NOK/MWh | integer | Price of secondary reserves for weekends |

## Processed dataset

### Variables

| Variable | Unit | Type | Description |
| -------- | ---- | ---- | ----------- |
