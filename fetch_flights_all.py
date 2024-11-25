import requests
from requests.auth import HTTPBasicAuth

import psycopg2
from psycopg2 import sql

from dotenv import load_dotenv
import os

url = "https://opensky-network.org/api/flights/all"

load_dotenv()

username = os.getenv("OPENSKY_USERNAME")
password = os.getenv("OPENSKY_PASSWORD")
db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")

db_config = {
    "dbname": "flight_data",
    "user": db_username,
    "password": db_password,
    "host": "localhost",
    "port": 5432
}

try:
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    response = requests.get(url, auth=(username, password))

    if response.status_code == 200:
        data = response.json()

        for info in data:
            cursor.execute(sql.SQL("""
            INSERT INTO flights_all(
                icao24, callsign, departure_airport, arrival_airport, departure_time, arrival_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """), (
                info["icao24"], 
                info["callsign"],
                info["estDepartureAirport"],
                info["estArrivalAirport"],
                info["firstSeen"],
                info["lastSeen"]
            )
            )
        
        conn.commit()
        print("data inserted succesfully into flights_all table")
    
    else:
        print(f"faied to fetch data. HTTP status code: {response.status_code}")

except Exception as e:
    print(f"Error: {e}")

finally:
    if conn:
        cursor.close()
        conn.close()