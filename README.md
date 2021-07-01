# HOW TO:

To launch server part execute _server.bat_ file;

To launch client part execute _client.bat_ file.

### DB:

Sample of server database was taken from [official sqlite3 guide resource](https://www.sqlitetutorial.net/sqlite-sample-database/);

Client db similar to server except it has random data;

_chinook.db_ - server db;

_collection.db_ - client db.

### Settings:

_settings.py_ file responsible for the settings of client;

__table__ - argument for request;

__request__ - api string request;

__db_path__ - path to local database;

__recursion_depth__ - the number of times to repeat the statement on error;

__request_frequency__ - frequency of execution of the main instruction in seconds.