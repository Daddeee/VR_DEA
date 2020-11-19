import os
import json

from sets import Set
from tqdm import tqdm

def elaborate(routes):
	stops = Set()
	services_count = 0
	stops_count = 0
	for date in routes:
		services_count += len(routes[date])
		for stop in routes[date]:
			lat = stops[5]
			lng = stops[6]
			stops.add((lat,lng))

	stops_count = len(stops)

	return {}

# Prepare folder to store services
base_folder = "dicembre_lettere/data/"
if not os.path.exists(base_folder):
	os.makedirs(base_folder)

raw_folder = "dicembre_lettere/raw_data/"
for filename in os.listdir(raw_folder):
    if filename.endswith(".json"):
        filepath = os.path.join(raw_folder, filename)
        with open(filepath, "r") as read_file:
		    data = json.load(read_file)

		elaborated = elaborate(data)

		with open(os.path.join(base_folder, filename), "w") as write_file:
			json.dump(elaborated, write_file, default=str, indent=4, sort_keys=True)    
    else:
        continue