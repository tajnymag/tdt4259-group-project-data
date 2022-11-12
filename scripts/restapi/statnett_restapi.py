from enum import Enum
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Any, Optional
import inspect
import re
import csv

from requests import get as http_get
from dacite import from_dict, Config

API_BASE_URL = "https://driftsdata.statnett.no/restapi"


def from_list(cls, data: list, config: Config = Config()) -> List:
    return [from_dict(cls, item, config) for item in data]


def only_numbers(string: str) -> str:
    return re.sub(r"[^0-9]", "", string)


class Country(Enum):
    ALL = "All"
    SWEDEN = "SE"
    DENMARK = "DK"
    NETHERLANDS = "NL"
    FINLAND = "FI"
    RUSSIA = "RU"
    GERMANY = "DE"
    UK = "EN"
    NORWAY = "NO"
    ESTONIA = "EE"
    LATVIA = "LV"
    LITHUANIA = "LT"


class Frequency(Enum):
    Hours = "Hours"
    Days = "Days"
    Weeks = "Weeks"
    Months = "Months"
    Years = "Years"
    Quarters = "Quarters"


class MeasurementType(Enum):
    MAX = "Max"
    MIN = "Min"
    MEDIAN = "Median"
    MEASUREMENT = "Measurement"


class ElSpot(Enum):
    NORWAY = "NO"
    NO1 = "NO1"
    NO2 = "NO2"
    NO3 = "NO3"
    NO4 = "NO4"
    NO5 = "NO5"


@dataclass()
class GetPhysicalFlowResponseRaw:
    PhysicalFlowNetExchange: List[Optional[float]]
    StartPointUTC: float
    EndPointUTC: float
    PeriodTickMs: int
    Frequency: Frequency
    Country: str


@dataclass()
class GetPhysicalFlowRow:
    measured_at: datetime
    country: Country
    physical_flow: float


def get_physical_flow_raw(from_date: datetime, to_date: datetime, frequency: Frequency,
                          country: Country) -> GetPhysicalFlowResponseRaw:
    path = "/PhysicalFlow/GetData"
    query = {
        "FromInTicks": int(from_date.timestamp() * 1000),
        "ToInTicks": int(to_date.timestamp() * 1000),
        "Frequency": frequency.value,
        "Country": country.value
    }
    res = http_get(f"{API_BASE_URL}/{path}", params=query)
    data = res.json()
    return from_dict(GetPhysicalFlowResponseRaw, data, Config(cast=[Country, Frequency]))


def get_physical_flow(from_date: datetime, to_date: datetime, frequency: Frequency, country: Country) -> List[GetPhysicalFlowRow]:
    data = get_physical_flow_raw(from_date, to_date, frequency, country)
    rows: List[GetPhysicalFlowRow] = []

    measured_at = datetime.fromtimestamp(data.StartPointUTC / 1000)

    for physical_flow in data.PhysicalFlowNetExchange:
        rows.append(
            GetPhysicalFlowRow(
                measured_at, Country(str.upper(data.Country) if data.Country != "" else Country.ALL), physical_flow
            )
        )
        measured_at += timedelta(milliseconds=data.PeriodTickMs)

    return rows


@dataclass()
class GetProductionConsumptionResponseRaw:
    Production: List[float]
    Consumption: List[float]
    StartPointUTC: float
    EndPointUTC: float
    PeriodTickMs: int


@dataclass()
class GetProductionConsumptionRow:
    measured_at: datetime
    production: float
    consumption: float


def get_production_consumption_raw(from_date: datetime, to_date: datetime,
                                   frequency: Frequency) -> GetProductionConsumptionResponseRaw:
    path = "/ProductionConsumption/GetData"
    query = {
        "FromInTicks": from_date.timestamp() * 1000,
        "ToInTicks": to_date.timestamp() * 1000,
        "Frequency": frequency.value
    }
    res = http_get(f"{API_BASE_URL}/{path}", params=query)
    data = res.json()
    return from_dict(GetProductionConsumptionResponseRaw, data)


def get_production_consumption(from_date: datetime, to_date: datetime, frequency: Frequency) -> List[GetProductionConsumptionRow]:
    data = get_production_consumption_raw(from_date, to_date, frequency)
    rows: List[GetProductionConsumptionRow] = []

    measured_at = datetime.fromtimestamp(data.StartPointUTC / 1000)

    for [production, consumption] in zip(data.Production, data.Consumption):
        rows.append(
            GetProductionConsumptionRow(
                measured_at, production, consumption
            )
        )
        measured_at += timedelta(milliseconds=data.PeriodTickMs)

    return rows


@dataclass()
class GetProductionConsumptionDetailedResponseRaw:
    @dataclass()
    class __TableItem:
        value: str
        textTranslationId: Optional[str]
        titleTranslationId: Optional[str]
        style: Optional[str]

    MeasuredAt: float
    Headers: List[__TableItem]
    ProductionData: List[__TableItem]
    NuclearData: List[__TableItem]
    HydroData: List[__TableItem]
    WindData: List[__TableItem]
    NotSpecifiedData: List[__TableItem]
    ConsumptionData: List[__TableItem]
    NetExchangeData: List[__TableItem]


@dataclass()
class GetProductionConsumptionDetailedRow:
    measured_at: datetime
    country: Country
    production: int
    consumption: int
    hydro: Optional[int]
    wind: int
    nuclear: Optional[int]
    unspecified: Optional[int]
    net_exchange: int


def get_production_consumption_detailed_raw(date: datetime) -> GetProductionConsumptionDetailedResponseRaw:
    path = "/ProductionConsumption/GetLatestDetailedOverview"
    query = {
        "timestamp": date.timestamp() * 1000
    }
    res = http_get(f"{API_BASE_URL}/{path}", params=query)
    data = res.json()
    return from_dict(GetProductionConsumptionDetailedResponseRaw, data)


def get_production_consumption_detailed(date: datetime) -> List[GetProductionConsumptionDetailedRow]:
    data = get_production_consumption_detailed_raw(date)
    rows: List[GetProductionConsumptionDetailedRow] = []
    for i in range(len(data.Headers))[1:-1]:
        measured_at = datetime.fromtimestamp(data.MeasuredAt / 1000)
        country = Country(data.Headers[i].value)
        production = int(only_numbers(data.ProductionData[i].value))
        consumption = int(only_numbers(data.ConsumptionData[i].value))
        hydro = int(only_numbers(data.HydroData[i].value)) if data.HydroData[i].value != "-" else None
        wind = int(only_numbers(data.WindData[i].value))
        nuclear = int(only_numbers(data.NuclearData[i].value)) if data.NuclearData[i].value != "-" else None
        unspecified = int(only_numbers(data.NotSpecifiedData[i].value)) if data.NotSpecifiedData[i].value != "-" else None
        net_exchange = int(only_numbers(data.NetExchangeData[i].value))

        rows.append(
            GetProductionConsumptionDetailedRow(
                measured_at, country, production, consumption, hydro, wind, nuclear, unspecified, net_exchange
            )
        )
    return rows


def get_utility_frequency_raw(from_date: datetime, to_date: datetime) -> List[tuple[int, int]]:
    path = "/Frequency/BySecondWithXy"
    query = {
        "FromInTicks": from_date.timestamp() * 1000,
        "ToInTicks": to_date.timestamp() * 1000
    }
    res = http_get(f"{API_BASE_URL}/{path}", params=query)
    data = res.json()
    return [(item[0], item[1]) for item in data["Measurements"]]


@dataclass()
class GetUtilityFrequencyRow:
    measured_at: datetime
    frequency: int


def get_utility_frequency(from_date: datetime, to_date: datetime) -> List[GetUtilityFrequencyRow]:
    data = get_utility_frequency_raw(from_date, to_date)
    rows: List[GetUtilityFrequencyRow] = []
    for [measured_at, frequency] in data:
        rows.append(
            GetUtilityFrequencyRow(
                datetime.fromtimestamp(measured_at / 1000), frequency
            )
        )
    return rows


@dataclass()
class GetReservoirItemRaw:
    fromYear: int
    toYear: int
    type: MeasurementType
    countryTotalData: List[float]
    elspot1Data: List[float]
    elspot2Data: List[float]
    elspot3Data: List[float]
    elspot4Data: List[float]
    elspot5Data: List[float]


@dataclass()
class GetReservoirRow:
    measured_at: datetime
    region: ElSpot
    type: MeasurementType
    value: float


def get_reservoir_raw(include_median=True, include_max=True, include_min=True) -> List[GetReservoirItemRaw]:
    path = "/Reservoir/"
    query = {
        "IncludeMedian": include_median,
        "IncludeMax": include_max,
        "IncludeMin": include_min
    }
    res = http_get(f"{API_BASE_URL}/{path}", params=query)
    data = res.json()
    return from_list(GetReservoirItemRaw, data, Config(cast=[MeasurementType]))


def get_reservoir(include_median=True, include_max=True, include_min=True) -> List[GetReservoirRow]:
    data = get_reservoir_raw(include_median, include_max, include_min)
    rows: List[GetReservoirRow] = []
    for item in data:
        regions = [ElSpot.NORWAY, ElSpot.NO1, ElSpot.NO2, ElSpot.NO3, ElSpot.NO4, ElSpot.NO5]
        region_data = [item.countryTotalData, item.elspot1Data, item.elspot2Data, item.elspot3Data, item.elspot4Data, item.elspot5Data]
        for [region, measurements] in zip(regions, region_data):
            week = 1
            for measurement in measurements:
                if item.type != MeasurementType.MEASUREMENT:
                    continue

                measured_at = datetime.fromisocalendar(item.fromYear, week, 1)
                rows.append(
                    GetReservoirRow(
                        measured_at=measured_at, region=region, type=item.type, value=measurement
                    )
                )
                week += 1

    return rows


@dataclass()
class GetPowerSituationsResponseItemRaw:
    elspotId: ElSpot
    powerSituation: str


@dataclass()
class GetPowerSituationsRow:
    measured_at: datetime
    region: ElSpot
    power_situation: str


def get_power_situations_raw(date: datetime) -> List[GetPowerSituationsResponseItemRaw]:
    path = "/ElspotPowerSituation/GetPowerSituations"
    query = {
        "timestamp": date.timestamp() * 1000,
        "localDate": date.strftime("%Y-%m-%d")
    }
    res = http_get(f"{API_BASE_URL}/{path}", params=query)
    data = res.json()
    return from_list(GetPowerSituationsResponseItemRaw, data, Config(cast=[ElSpot]))


def get_power_situations(date: datetime) -> List[GetPowerSituationsRow]:
    data = get_power_situations_raw(date)
    rows: List[GetPowerSituationsRow] = []
    for item in data:
        rows.append(
            GetPowerSituationsRow(
                measured_at=date, region=item.elspotId, power_situation=item.powerSituation
            )
        )
    return rows


@dataclass()
class GetPowerSituationsChangesResponseRaw:
    Changes: List[float]


def get_power_situations_changes_raw(number_of_changes: int, date: datetime) -> GetPowerSituationsChangesResponseRaw:
    path = "/ElspotPowerSituation/LastChanges"
    query = {
        "numberOfChanges": number_of_changes,
        "timestamp": date.timestamp() * 1000,
    }
    res = http_get(f"{API_BASE_URL}/{path}", params=query)
    data = res.json()
    return from_dict(GetPowerSituationsChangesResponseRaw, data)

