import sys
import urllib.request
import time
from flask import json
import sqlite3
import re
import settings


def api_request(request, *args):
    """
    Function to get data from api url request.

    :param request: string url request;
    :param args: utility args to parse filtered data from request;

    :return: list of data maps.
    """
    with urllib.request.urlopen(request) as url:
        data = json.loads(url.read().decode())
    for arg in args:
        data = data.get(arg)
    return data


def heartbeat(db, req, arg, depth, rec_count, freq):
    """
    The main client function that receives API data and puts it into a local database.

    :param db: string database path;
    :param req: string url request;
    :param arg: string table name;
    :param depth: int max error recursion depth;
    :param rec_count: int current error recursion depth;
    :param freq: frequency of function working.
    """
    conn = create_connection(db)
    cursor = conn.cursor()
    req = api_request(req)
    while True:
        try:
            parse_result = request_parser(req)
            query = f"INSERT INTO {arg} ({parse_result[1]}) VALUES ({parse_result[2]})"
            cursor.executemany(query, parse_result[0])
            conn.commit()
            time.sleep(freq)
        except Exception as ex:
            print(ex)
            if rec_count < depth:
                heartbeat(db, req, arg, depth, rec_count + 1, freq)
            else:
                print("Maximum error recursion depth.")
                sys.exit()


def request_parser(req_list):
    """
    Function to prepare url request data for insertion into local database.

    :param req_list: list with maps of data from api request;

    :return: tuple of lists of rows, columns and question marks.
    """
    cols = ""
    qm = ""
    items = []
    for item in req_list:
        values = []
        for key in item:
            if re.search(r'Id', key) is None:
                values.append(item[key])
                if key not in cols:
                    cols += f"{key}, "
                    qm += "?, "
        items.append(values)

    return items, cols[:-2], qm[:-2]


def create_connection(db_file):
    """
    Safe method to create sqlite connection.

    :param db_file: string path to sqlite3 database;

    :return: sqlite connection.
    """
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        print(sqlite3.version)
    except sqlite3.Error as e:
        print(e)

    return connection


if __name__ == "__main__":
    recursion_counter = 0
    heartbeat(
        settings.db_path,
        settings.request,
        settings.table,
        settings.recursion_depth,
        recursion_counter,
        settings.request_frequency
    )
