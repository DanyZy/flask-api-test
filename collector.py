import urllib.request
import time
from flask import json
import sqlite3


def api_request(request, *args):
    with urllib.request.urlopen(request) as url:
        data = json.loads(url.read().decode())
    for arg in args:
        data = data.get(arg)
    return data


table = "employees"
req = api_request(f"http://127.0.0.1:5000/api/v1/entries/{table}/all")


def heartbeat(cursor):
    while True:
        try:
            for item in req:
                columns = ""
                qm = ""
                vals = []
                for key in item:
                    columns += key + ", "
                    qm += "?, "
                    vals.append(item[key])
                columns = columns[:-2]
                qm = qm[:-2]
                query = f"INSERT INTO {table} ({columns}) VALUES ({qm})"
                cursor.execute(query, vals).fetchall()
            time.sleep(10)
        except Exception as ex:
            print(ex)
            heartbeat(cursor)


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except sqlite3.Error as e:
        print(e)

    return conn


if __name__ == "__main__":
    cur = create_connection("collection.db").cursor()
    heartbeat(cur)
