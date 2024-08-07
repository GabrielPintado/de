import requests
import pandas as pd
import psycopg2
from psycopg2 import sql

api_key = 'ba7260fc7c657b11720a81e5471e7d14'  
base_url = "http://api.openweathermap.org/data/2.5/weather"
cities = ["New York", "Los Angeles", "Chicago", "Houston", "Atlanta"]
weather_data = []

for city in cities:
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'  
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        weather_info = {
            'city': city,
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'weather': data['weather'][0]['description'],
            'timestamp': pd.to_datetime(data['dt'], unit='s')
        }
        weather_data.append(weather_info)
    else:
        print(f"Error al obtener datos para {city}: {response.status_code}")

df = pd.DataFrame(weather_data)


redshift_endpoint = 'data-engineer-cluster.cyhh5bfevlmn.us-east-1.redshift.amazonaws.com'
redshift_port = '5439'
redshift_dbname = 'data-engineer-database'
redshift_user = 'gabrielpin25_coderhouse'
redshift_password = '00b99Uzw8s'

conn = psycopg2.connect(
    dbname=redshift_dbname,
    user=redshift_user,
    password=redshift_password,
    host=redshift_endpoint,
    port=redshift_port
)
cursor = conn.cursor()


create_table_query = """
CREATE TABLE IF NOT EXISTS weather_data (
    city VARCHAR(50),
    temperature FLOAT,
    humidity INT,
    weather VARCHAR(50),
    timestamp TIMESTAMP
);
"""

cursor.execute(create_table_query)
conn.commit()


insert_query = """
INSERT INTO weather_data (city, temperature, humidity, weather, timestamp)
VALUES (%s, %s, %s, %s, %s)
"""

for index, row in df.iterrows():
    cursor.execute(insert_query, (row['city'], row['temperature'], row['humidity'], row['weather'], row['timestamp']))

conn.commit()
cursor.close()
conn.close()

print("Datos cargados exitosamente en Redshift.")
