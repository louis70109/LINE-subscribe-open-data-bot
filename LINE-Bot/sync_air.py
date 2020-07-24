## http://opendata.epa.gov.tw/webapi/Data/REWIQA/?$orderby=SiteName&$skip=0&$top=1000&format=json

import requests

air_data = requests.get(
    'http://opendata.epa.gov.tw/webapi/Data/REWIQA/?$orderby=SiteName&$skip=0&$top=1000&format=json')

airs = air_data.json()
status = ["良好", "普通", "對敏感族群不健康", "對所有族群不健康", "非常不健康", "危害", "資料有誤"]
average = [50, 100, 150, 200, 250, 300]
taichung = []
for air in airs:
    if air.get('County') == '臺中市':
        taichung.append(air)

sum, count = 0, 0

for t in taichung:
    if t['SiteName'] == "西屯" or t['SiteName'] == "沙鹿":
        count += 1
        if t['AQI'] != 0:
            sum += int(t['AQI'])

sw = 0
total = sum / count

if total >= 0 and total <= 50:
    payload = f"\n空氣品質: {status[0]}"
elif total >= 51 and total <= 100:
    payload = f"\n空氣品質: {status[1]}"
elif total >= 101 and total <= 150:
    payload = f"\n空氣品質: {status[2]}"
elif total >= 151 and total <= 200:
    payload = f"\n空氣品質: {status[3]}"
elif total >= 201 and total <= 250:
    payload = f"\n空氣品質: {status[4]}"
elif total >= 251 and total <= 300:
    payload = f"\n空氣品質: {status[5]}"
else:
    payload = f"\n空氣品質: {status[6]}"

print(payload)