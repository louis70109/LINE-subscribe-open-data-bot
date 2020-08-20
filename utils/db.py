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


def find_counties():
    with Database() as db, db.connect() as conn, conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute('SELECT * FROM taiwan order by county')
        rows = cur.fetchall()
    county = []
    tmp = ''
    for row in rows:
        if tmp != row['county']:
            county.append(row)

        tmp = row['county']

    return county


def find_sites_by_county(county):
    with Database() as db, db.connect() as conn, conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(f''' SELECT * FROM taiwan WHERE county = '{county}' ''')
        rows = cur.fetchall()

    return rows


def find_site(site):
    with Database() as db, db.connect() as conn, conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(f''' SELECT * FROM taiwan WHERE site_name = '{site}' ''')
        row = cur.fetchone()

    return row


def find_user_site(line_id, site):
    with Database() as db, db.connect() as conn, conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(
            f'''
                SELECT * FROM user_site WHERE line_id = '{line_id}' and site_name = '{site}'
            ''')
        row = cur.fetchone()

    return row


def create_user_site(line_id, site):
    with Database() as db, db.connect() as conn, conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(f'''
                INSERT INTO user_site (line_id, site_name)
                  VALUES (
                    '{line_id}', 
                    '{site}'
                );''')
        conn.commit()


def remove_user_site(line_id, site):
    with Database() as db, db.connect() as conn, conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(f"DELETE FROM user_site WHERE line_id = '{line_id}' and site_name = '{site}'")
        conn.commit()


def create_user_notify(line_id, token):
    with Database() as db, db.connect() as conn, conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(f'''
            INSERT INTO "user" (line_id, notify_token)
              VALUES (
                '{line_id}', 
                '{token}'
            ) ON CONFLICT user_pkey
            ON CONFLICT ON CONSTRAINT user_pkey 
            DO UPDATE SET notify_token='{token}' WHERE lottery.line_id='{line_id}'
        ''')
        conn.commit()


def find_user_notify_info(line_id):
    with Database() as db, db.connect() as conn, conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(f''' SELECT * FROM "user" WHERE line_id = '{line_id}' ''')
        row = cur.fetchone()

    return row
