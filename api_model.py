import sqlite3
from flask import request, jsonify


class API:
    """API model class for connecting and querying to sqlite3 database."""

    def __init__(self, db_file, data_format):
        self.__create_connection(db_file)
        self.conn.row_factory = data_format
        self.cur = self.conn.cursor()
        self.tables = self.__get_tables()

    def __create_connection(self, db_file):
        """
        Safe method to create sqlite connection.

        :param db_file: string path to sqlite3 database.
        """
        try:
            self.conn = sqlite3.connect(db_file)
            print(sqlite3.version)
        except sqlite3.Error as e:
            print(e)

    def get_all(self, table, error_handler):
        """
        A method to get all rows from a table.

        :param table: string name of table;
        :param error_handler: function to handle filter error;

        :return: json array with all items of request if table parameter in table list field;
        :return: result on error handler function if table parameter not in table list field.
        """
        if table in [val['name'] for val in self.tables]:
            results = self.cur.execute(f'SELECT * FROM {table};').fetchall()

            return jsonify(results)
        else:
            return error_handler

    def get_with_filter(self, table, error_handler, filter_enum):
        """
        A method for getting filtered rows from a table.

        :param table: string name of table;
        :param error_handler: function to handle filter error;
        :param filter_enum: map where key - request name and value - table name;

        :return: json array with filtered items of request if table parameter in table list field;
        :return: result on error handler function if table parameter not in table list field or
        if request name of filter not in filter map.
        """
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
        """
        A method to get the names of all tables from the database.

        :return: string list of table names.
        """
        query = "SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';"
        result = self.cur.execute(query).fetchall()

        return result
