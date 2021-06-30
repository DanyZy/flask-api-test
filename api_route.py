import flask
from api_model import API


app = flask.Flask(__name__)
app.config["DEBUG"] = True
filter_enum = {}


def dict_factory(cursor, row):
    """
    Pattern function for row factory of database.

    :param cursor: sqlite cursor object;
    :param row: database row;

    :return: map where key - table name and value - value of row in table.
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# Route functions:
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/', methods=['GET'])
def index():
    return "<h1>Proto API</h1>" \
           "<p>This site is a prototype for API testing based on Flask framework.</p>"


@app.route('/api/v1/entries/<table>/all', methods=['GET'])
def api_all(table):
    api = API('chinook.db', dict_factory)
    return api.get_all(table, page_not_found(404))


@app.route('/api/v1/entries/<table>', methods=['GET'])
def api_filter(table):
    api = API('chinook.db', dict_factory)
    return api.get_with_filter(table, page_not_found(404), filter_enum)
# End of route functions


if __name__ == "__main__":
    filter_enum = {
        'employee_id': "EmployeeId",
        'last_name': "LastName",
        'reports_to': "ReportsTo",
    }
    app.run()
