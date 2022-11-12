#!/usr/bin/env python

from datetime import datetime, timedelta
import csv
import os

import statnett_restapi as statnett

OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "datasets")

START_DATE = datetime(2019, 1, 1)
END_DATE = datetime.now()


def scrape_physical_flow(from_date: datetime, to_date: datetime, output_file_path: str):
    with open(output_file_path, "w") as f:
        field_names = ["Time(Local)", "Country", "Flow"]
        csv_writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        csv_writer.writerow(field_names)
        for country in [statnett.Country.ALL, statnett.Country.SWEDEN, statnett.Country.DENMARK, statnett.Country.NETHERLANDS, statnett.Country.FINLAND, statnett.Country.RUSSIA, statnett.Country.GERMANY, statnett.Country.UK]:
            physical_flow_data = statnett.get_physical_flow(from_date, to_date, statnett.Frequency.Hours, country)
            for row in physical_flow_data:
                csv_writer.writerow([row.measured_at, row.country.value, row.physical_flow])


def scrape_reservoirs(output_file_path: str):
    with open(output_file_path, "w") as f:
        field_names = ["Time(Local)", "Area", "Type", "Volume"]
        csv_writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        csv_writer.writerow(field_names)
        reservoir_data = statnett.get_reservoir()
        for row in reservoir_data:
            csv_writer.writerow([row.measured_at, row.region.value, row.type.value, row.value])


def scrape_power_situations(from_date: datetime, to_date: datetime, output_file_path: str, period: timedelta = timedelta(days=1)):
    with open(output_file_path, "w") as f:
        field_names = ["Time(Local)", "Area", "Situation"]
        csv_writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        csv_writer.writerow(field_names)
        measured_at = from_date
        while measured_at < to_date:
            print(f"Scraping power situation data for {measured_at}")
            power_situation_data = statnett.get_power_situations(measured_at)
            for row in power_situation_data:
                csv_writer.writerow([row.measured_at, row.region.value, row.power_situation])
            measured_at += period


def main():
    print(f"Scraping physical flow data since {START_DATE}")
    scrape_physical_flow(START_DATE, END_DATE, os.path.join(OUTPUT_DIR, "physical_flow_per_country.csv"))

    print(f"Scraping reservoir data")
    scrape_reservoirs(os.path.join(OUTPUT_DIR, "hydro_reservoirs.csv"))

    print(f"Scraping power situations since {START_DATE}")
    scrape_power_situations(START_DATE, END_DATE, os.path.join(OUTPUT_DIR, "power_situations.csv"))


if __name__ == "__main__":
    main()
