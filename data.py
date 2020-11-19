import psycopg2
import pymssql
import os
import json
from datetime import datetime
from tqdm import tqdm
from dotenv import load_dotenv

# Load database credentials
load_dotenv(verbose=True)

# Prepare folder to store services
base_folder = "primo_semestre/raw_data/"
if not os.path.exists(base_folder):
	os.makedirs(base_folder)

# Connect to mssql database
conn = pymssql.connect(server=os.getenv("DB_SERVER"), user=os.getenv("DB_USER"), 
	password=os.getenv("DB_PASSWORD"), database=os.getenv("DB_DATABASE"))  

# Retrieve all different drivers. TODO: handle duplicates
cur = conn.cursor()
cur.execute("""
	SELECT DISTINCT(Postino)
	FROM nexive_consegne
	INNER JOIN nexive_servizio ON nexive_consegne.Servizio = nexive_servizio.idservizio
	INNER JOIN nexive_tipologieservizio ON nexive_servizio.idtipologia = nexive_tipologieservizio.idtipologia
""")

drivers = [d[0] for d in cur.fetchall() if d[0] is not None ]

# Retrieve services of each driver
for dname in tqdm(drivers):

	cur.execute("""
		SELECT *
		FROM nexive_consegne
		JOIN nexive_servizio ON nexive_consegne.Servizio = nexive_servizio.idservizio
		JOIN nexive_tipologieservizio ON nexive_servizio.idtipologia = nexive_tipologieservizio.idtipologia
		WHERE nexive_consegne.Postino = '{0}'
		ORDER BY DataRecapito ASC
	""".format(dname.replace("'", "''")))
	result = cur.fetchall()

	# Group services by date, creating a "giro"
	result_dict = {}
	for service in result:
		delivery_datetime = datetime.strptime(service[11].split(".")[0], "%Y-%m-%d %H:%M:%S") 
		date = delivery_datetime.strftime("%Y/%m/%d")
		result_dict.setdefault(date, []).append(service)

	# dump it to json
	with open(base_folder + dname + ".json", "w") as write_file:
		json.dump(result_dict, write_file, default=str, indent=4, sort_keys=True)