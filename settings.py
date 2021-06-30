"""File with settings for client."""

table = "employees"
request = f"http://127.0.0.1:5000/api/v1/entries/{table}/all"
db_path = "collection.db"
recursion_depth = 2
request_frequency = 10  # in seconds
