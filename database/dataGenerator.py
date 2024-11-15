import database.model as md
from datetime import datetime, timedelta
import csv

if __name__ == "__main__":
    end = datetime(2024, 11, 14, 14, 54, 45)

    current_time = end

    with open ('output.csv', newline='') as csvfile:
        csvreader = csv.reader(csvfile)

        header = next(csvreader)

        for row in csvreader:
            methane = row[0]
            carbon = row[1]
            air = row[2]
            butane = row[3]
            
            gas_levels = {
                10: float(methane),
                4: float(carbon),
                1: float(air),
                3: float(butane)
            }
            latitude = 44.3148443
            longitude = -85.6023643
            md.insert_gasses_with_timestamp (gas_levels, current_time, latitude, longitude)
            current_time -= timedelta(seconds=30)