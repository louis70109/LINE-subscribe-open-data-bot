import requests
import psycopg2
import psycopg2.extras

from apscheduler.schedulers.blocking import BlockingScheduler
import urllib.parse as urlparse
import os

from lotify.client import Client

sched = BlockingScheduler()

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


@sched.scheduled_job('cron', day_of_week='mon-fri', minute='*/1')
def notify_me():
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


@sched.scheduled_job('cron', day_of_week='mon-fri', minute='*/30')
def sync_to_db():
    print('Check tables status...')
    try:
        with Database() as db, db.connect() as conn, conn.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(f'''
                CREATE TABLE public.taiwan
                (
                    site_name character varying(20) COLLATE pg_catalog."default" NOT NULL,
                    county character varying(20) COLLATE pg_catalog."default",
                    aqi character varying(10) COLLATE pg_catalog."default" DEFAULT 0,
                    status character varying(15) COLLATE pg_catalog."default",
                    update_time character varying(20) COLLATE pg_catalog."default",
                    CONSTRAINT taiwan_pkey PRIMARY KEY (site_name)
                );
                CREATE TABLE public.user_site
                (
                    line_id character varying(50) COLLATE pg_catalog."default",
                    site_name character varying(20) COLLATE pg_catalog."default",
                    CONSTRAINT site UNIQUE (site_name)
                );
                CREATE TABLE public."user"
                (
                    line_id character varying(50) COLLATE pg_catalog."default" NOT NULL,
                    notify_token character varying(100) COLLATE pg_catalog."default" NOT NULL,
                    CONSTRAINT user_pkey PRIMARY KEY (line_id)
                )
                TABLESPACE pg_default;
                
                ALTER TABLE public.taiwan
                    OWNER to {USER};
                ALTER TABLE public."user"
                    OWNER to {USER};
                ALTER TABLE public.user_site
                    OWNER to {USER};
            ''')
            conn.commit()
    except psycopg2.errors.DuplicateTable:
        print('Tables have been create.')
        pass
    except Exception as e:
        raise Exception(e)

    print('Search data......')
    air_data = requests.get(
        'http://opendata.epa.gov.tw/webapi/Data/REWIQA/?$orderby=SiteName&$skip=0&$top=1000&format=json')

    airs = air_data.json()
    if airs:
        print("Get data success")

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
