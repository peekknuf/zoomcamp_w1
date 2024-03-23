import os
import requests
from datetime import datetime
import time

base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{}-{}.parquet"

start_year = 2022
end_year = 2023

download_path = "/home/peek/code/ny_taxi_data"

for year in range(start_year, end_year + 1):
    for month in range(1, 13):
        formatted_url = base_url.format(year, str(month).zfill(2))
        filename = os.path.join(download_path, f"yellow_taxi_trips_{year}_{str(month).zfill(2)}.parquet")

        if not os.path.exists(filename):
            start_time = time.time()
            dataset_response = requests.get(formatted_url)

            if dataset_response.status_code == 200:
                with open(filename, "wb") as dataset_file:
                    dataset_file.write(dataset_response.content)
                end_time = time.time()

                duration = end_time - start_time
                print(f"Downloaded: {filename} (Time: {duration:.2f} seconds)")
            else:
                print(f"Failed to download: {filename}")
        else:
            print(f"File already exists, skipping: {filename}")
