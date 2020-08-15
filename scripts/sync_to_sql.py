import requests
import sqlite3
import os
import psycopg2
import psycopg2.extras

class Database():
    conns = []

    def __enter__(self):
        return self

    def connect(self):
        import urllib.parse as urlparse
        import os

        url = urlparse.urlparse(os.getenv('DATABASE_URL'))
        dbname = url.path[1:]
        user = url.username
        password = url.password
        host = url.hostname
        port = url.port

        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.conns.append(conn)

        return conn

    def __exit__(self, type, value, traceback):
        for conn in self.conns:
            conn.close()

        self.conns.clear()


air_data = requests.get(
    'http://opendata.epa.gov.tw/webapi/Data/REWIQA/?$orderby=SiteName&$skip=0&$top=1000&format=json')

airs = air_data.json()
if airs:
    print("Get data success")
taichung = []

print("Connecting...")
print("Sync date to DB!!")
with Database() as db, db.connect() as conn, conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor) as cur:
    for air in airs:
        cur.execute(f'''
            INSERT INTO taiwan (site_name, county, aqi, status, update_time)
              VALUES (
                '{air.get('SiteName')}', 
                '{air.get('County')}', 
                '{air.get('AQI')}',
                '{air.get('Status')}',
                '{air.get('PublishTime')}'
            ) ON CONFLICT ON CONSTRAINT taiwan_pkey
            DO UPDATE SET
            county = '{air.get('County')}',
            aqi = '{air.get('AQI')}',
            status = '{air.get('Status')}',
            update_time = '{air.get('PublishTime')}'
        ''')
    conn.commit()
print("Closing...Bye")
conn.close()
