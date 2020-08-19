from lotify.client import Client
import psycopg2
import psycopg2.extras

import urllib.parse as urlparse
import os


URL = urlparse.urlparse(os.getenv('DATABASE_URL'))
DB_NAME = URL.path[1:]
USER = URL.username
PASSWORD = URL.password
HOST = URL.hostname
PORT = URL.port


class Database:
    conns = []

    def __enter__(self):
        return self

    def connect(self):
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT
        )
        self.conns.append(conn)

        return conn

    def __exit__(self, type, value, traceback):
        for conn in self.conns:
            conn.close()

        self.conns.clear()


lotify = Client()
print("Connecting...")
print("Cursor start...")
with Database() as db, db.connect() as conn, conn.cursor(
        cursor_factory=psycopg2.extras.RealDictCursor) as cur:
    cur.execute(f'''
        SELECT "user".notify_token, user_site.* from "user" LEFT JOIN user_site ON "user".line_id = user_site.line_id
    ''')
    users = cur.fetchall()
    cur.execute(f'''
        SELECT  us.line_id, taiwan.* from user_site as us LEFT JOIN taiwan ON us.site_name = taiwan.site_name
    ''')
    sites = cur.fetchall()
    print("Fetch data success!")
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
