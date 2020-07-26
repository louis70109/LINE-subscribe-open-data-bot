import os
import sqlite3


def find_counties():
    conn = sqlite3.connect(os.path.abspath('Air.db'))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT * FROM taichung GROUP BY county')
    rows = cur.fetchall()
    conn.close()
    return rows


def find_sites(county):
    conn = sqlite3.connect(os.path.abspath('Air.db'))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        f'''
        SELECT * FROM taichung WHERE county = "{county}"
    ''')
    rows = cur.fetchall()
    conn.close()
    return rows


def find_user_site(line_id, site):
    conn = sqlite3.connect(os.path.abspath('Air.db'))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        f'''
            SELECT * FROM user WHERE line_id = "{line_id}" and site_name = "{site}"
        ''')
    row = cur.fetchone()
    conn.close()
    return row


def create_user_site(line_id, site):
    conn = sqlite3.connect(os.path.abspath('Air.db'))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(f'''
            INSERT OR REPLACE INTO user (line_id, site_name)
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
    cur.execute(f'DELETE FROM user WHERE line_id = "{line_id}" and site_name = "{site}"')
    conn.commit()
    conn.close()
