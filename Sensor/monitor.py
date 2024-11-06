from serial import Serial
import csv
from datetime import datetime
import json

arduino_port = "COM7" #serial port of Arduino
baud = 9600 #arduino uno runs at 9600 baud
fileName="analog-data.csv" #name of the CSV file generated

ser = Serial(arduino_port, baud)
print("Connected to Arduino port:" + arduino_port)
print("Created file")


with open("output2.csv", 'a', encoding='UTF8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["methane", "carbonmonoxide", "airquality", "butane", "timestamp"])
    writer.writeheader()

    while True:
        getData=ser.readline()
        dataString = getData.decode('utf-8')
        data=dataString[0:][:-2]
        

        data = dict(json.loads(data))
        

        timestamp = datetime.now().strftime ('%H:%M:%S')
        data['timestamp'] = timestamp
        writer.writerow(data)