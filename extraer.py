import psycopg2
import pandas as pd

conn = psycopg2.connect(
    dbname='data-engineer-database',
    user='gabrielpin25_coderhouse',
    password='00b99Uzw8s',
    host='data-engineer-cluster.cyhh5bfevlmn.us-east-1.redshift.amazonaws.com',
    port='5439'
)

query = "SELECT * FROM weather_data LIMIT 100;"

df = pd.read_sql_query(query, conn)

df.to_csv('weather_data_sample.csv', index=False)

conn.close()

print("Muestra de datos guardada en 'weather_data_sample.csv'.")
