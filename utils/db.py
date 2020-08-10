import os
import sqlite3


def find_counties():
    conn = sqlite3.connect(os.path.abspath('Air.db'))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT * FROM taiwan GROUP BY county')
    rows = cur.fetchall()
    conn.close()
    return rows


def find_sites_by_county(county):
    conn = sqlite3.connect(os.path.abspath('Air.db'))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(f''' SELECT * FROM taiwan WHERE county = "{county}" ''')
    rows = cur.fetchall()
    conn.close()
    return rows


def find_site(site):
    conn = sqlite3.connect(os.path.abspath('Air.db'))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(f''' SELECT * FROM taiwan WHERE site_name = "{site}" ''')
    row = cur.fetchone()
    conn.close()
    return row


def find_user_site(line_id, site):
    conn = sqlite3.connect(os.path.abspath('Air.db'))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        f'''
            SELECT * FROM user_site WHERE line_id = "{line_id}" and site_name = "{site}"
        ''')
    row = cur.fetchone()
    conn.close()
    return row


def create_user_site(line_id, site):
    conn = sqlite3.connect(os.path.abspath('Air.db'))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(f'''
            INSERT INTO user_site (line_id, site_name)
              VALUES (
                "{line_id}", 
                "{site}"
            );''')
    conn.commit()
    conn.close()


def remove_user_site(line_id, site):
    conn = sqlite3.connect(os.path.abspath('Air.db'))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(f'DELETE FROM user_site WHERE line_id = "{line_id}" and site_name = "{site}"')
    conn.commit()
    conn.close()


def create_user_notify(line_id, token):
    conn = sqlite3.connect(os.path.abspath('Air.db'))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(f'''
            INSERT OR REPLACE INTO user (line_id, notify_token)
              VALUES (
                "{line_id}", 
                "{token}"
            )''')
    conn.commit()
    conn.close()


def find_user_notify_info(line_id):
    conn = sqlite3.connect(os.path.abspath('Air.db'))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(f''' SELECT * FROM user WHERE line_id = "{line_id}" ''')
    row = cur.fetchone()
    conn.close()
    return row
