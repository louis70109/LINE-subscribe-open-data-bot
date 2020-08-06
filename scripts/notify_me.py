import os
import sqlite3
from lotify.client import Client

lotify = Client()
print("Connecting...")
try:
    conn = sqlite3.connect(os.path.abspath('Air.db'))
    conn.row_factory = sqlite3.Row
except:
    raise ValueError("Connect SQLite error")
c = conn.cursor()
print("Cursor start...")

c.execute(f'''
    SELECT user.notify_token, user_site.* from user LEFT JOIN user_site ON user.line_id = user_site.line_id
''')
users = c.fetchall()
c.execute(f'''
    SELECT  us.line_id, taiwan.*  from user_site as us LEFT JOIN taiwan ON us.site_name = taiwan.site_name
''')
sites = c.fetchall()
print("Fetch data success!")
conn.close()
print('Close connection')
messages = ''
already = []
for user in users:
    for site in sites:
        if user['line_id'] in already:
            break
        if user['line_id'] == site['line_id']:
            messages += f'''\n{site['county']}/{site['site_name']} ➡ ️{site['status']}'''
    if user['line_id'] not in already:
        lotify.send_message(access_token=user['notify_token'], message=messages)
        already.append(user['line_id'])
        messages = ''
print('Notifications have been send.')
