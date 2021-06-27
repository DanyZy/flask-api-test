import sqlite3
from flask import request, jsonify


class API:

    def __init__(self, db_file, data_format):
        self.__create_connection(db_file)
        self.conn.row_factory = data_format
        self.cur = self.conn.cursor()
        self.tables = self.__get_tables()

    def __create_connection(self, db_file):
        try:
            self.conn = sqlite3.connect(db_file)
            print(sqlite3.version)
        except sqlite3.Error as e:
            print(e)

    def get_all(self, table, error_handler):
        if table in [val['name'] for val in self.tables]:
            results = self.cur.execute(f'SELECT * FROM {table};').fetchall()

            return jsonify(results)
        else:
            return error_handler

    def get_with_filter(self, table, error_handler, filter_enum):
        if table in [val['name'] for val in self.tables]:
            query_parameters = request.args
            query = f"SELECT * FROM {table} WHERE"
            to_filter = []

            for filter_name in query_parameters:
                if filter_name in filter_enum:
                    query += ' ' + filter_enum.get(filter_name) + '=? AND'
                    to_filter.append(query_parameters.get(filter_name))
                else:
                    return error_handler

            query = query[:-4] + ';'

            results = self.cur.execute(query, to_filter).fetchall()

            return jsonify(results)
        else:
            return error_handler

    def __get_tables(self):
        query = "SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';"
        result = self.cur.execute(query).fetchall()

        return result
