## http://opendata.epa.gov.tw/webapi/Data/REWIQA/?$orderby=SiteName&$skip=0&$top=1000&format=json

import requests
import sqlite3
import os

air_data = requests.get(
    'http://opendata.epa.gov.tw/webapi/Data/REWIQA/?$orderby=SiteName&$skip=0&$top=1000&format=json')

airs = air_data.json()
if airs:
    print("Get data success")
taichung = []

conn = sqlite3.connect(os.path.abspath('../Air.db'))
print("Connecting...")
c = conn.cursor()
print("Sync date to DB!!")
for air in airs:
    c.execute(f'''
        INSERT OR REPLACE INTO taichung (site_name, county, aqi, status, update_time)
          VALUES (
            "{air.get('SiteName')}", 
            "{air.get('County')}", 
            "{air.get('AQI')}",
            "{air.get('Status')}",
            "{air.get('PublishTime')}"
        );
         ''')
    conn.commit()
print("Closing...Bye")
conn.close()
