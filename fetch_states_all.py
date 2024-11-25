import requests # library, which we use to send HTTP requests to the OpenSky API
from requests.auth import HTTPBasicAuth

import psycopg2 #library, which allows us to connect to and interact with a PostgreSQL database from Python
from psycopg2 import sql #helps to dynamically construct SQL queries in a safe way (prevents SQL injection when inserting user-provided data)

from dotenv import load_dotenv
import os #allows you to interact with the operating system

url = "https://opensky-network.org/api/states/all"

load_dotenv() # Load environment variables from the .env file

username = os.getenv("OPENSKY_USERNAME")
password = os.getenv("OPENSKY_PASSWORD")
db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")

#This dictionary contains the connection details for your PostgreSQL database:
db_config = {
    "dbname" : "flight_data",
    "user" : db_username,
    "password" : db_password,
    "host" : "localhost",
    "port" : 5432
}

try:
    conn = psycopg2.connect(**db_config) #Establishes a connection to your PostgreSQL database using the details in db_config
    cursor = conn.cursor() #Creates a cursor object that allows you to execute SQL commands in the database.

    response = requests.get(url, auth=(username, password))

    if response.status_code == 200:
        data = response.json()["states"]

        for state in data:
            # cursor.execute(query, values)
            cursor.execute(sql.SQl("""
            INSERT INTO states_all (
                icao24, callsign, origin_country, latitude, longitude, baro_altitude, geo_altitude, velocity, true_track, vertical_rate, on_ground, timestamp)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW());
            """), (
                state[0],
                state[1],
                state[2],
                state[6],
                state[5],
                state[7],
                state[13], 
                state[9],
                state[10],
                state[11], 
                state[8]
            ) )

        conn.commit()
        print("data inserted succesfully into states_all table")
    else:
        print(f"failed to fetch data. HTTP status code: {response.status_code}")

except Exception as e:
    print(f"Error: {e}")

finally:
    cursor.close()
    conn.close()

