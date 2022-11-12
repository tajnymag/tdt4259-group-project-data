#!/usr/bin/env python
import time
from datetime import datetime, timedelta
import csv
import os

import statnett_restapi as statnett

OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "datasets")


def scrape_production_consumption_detailed(to_date: datetime, output_file_path: str):
    measured_at = datetime.now()
    with open(output_file_path, "w") as f:
        field_names = ["Time(Local)", "Country", "Production", "Consumption", "Hydro", "Wind", "Nuclear", "Unspecified", "NetExchange"]
        csv_writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        csv_writer.writerow(field_names)
        while measured_at < to_date:
            print(f"Scraping production and consumption data for {measured_at}")
            production_consumption_data = statnett.get_production_consumption_detailed(measured_at)
            for row in production_consumption_data:
                csv_writer.writerow([row.measured_at, row.country.value, row.production, row.consumption, row.hydro, row.wind, row.nuclear, row.unspecified, row.net_exchange])
            time.sleep(60)
            measured_at = datetime.now()


def main():
    start_date = datetime.now()
    end_date = datetime.now() + timedelta(days=1, hours=12)
    print(f"Scraping production and consumption data since {start_date}")
    scrape_production_consumption_detailed(end_date, os.path.join(OUTPUT_DIR, "production_consumption.csv"))


if __name__ == "__main__":
    main()
