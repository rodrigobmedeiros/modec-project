import json

class SetDatabase():
    """
    class responsible to load database configuration from config.json file.
    """
    def __init__(self, json_file_path):
        """
        parameters:
        
        json_file_path (str): path to find the config file and get all information needed to connect to the database.
        """
        self.json_file_path = json_file_path
        self._database = None
        self._user = None
        self._password = None
        self._host = None
        self._port = None
        self._database_name = None
        self._connection_string = None
        self._read_config_file()
        self._mount_database_string()

    def _read_config_file(self):

        with open(self.json_file_path) as config_file:

            config_info = json.load(config_file)

        database_info = config_info["database_info"]

        self._database = database_info['database']
        self._user = database_info['user']
        self._password = database_info['password']
        self._host = database_info['host']
        self._port = database_info['port']
        self._database_name = database_info['database_name']

        return None

    def _mount_database_string(self):

        self._connection_string = ''.join(
            [
                self._database, 
                '://',
                self._user,
                ':',
                self._password,
                '@',
                self._host,
                ':',
                self._port, 
                '/',
                self._database_name
            ]
        )

        return None

    @property
    def connection_string(self):

        return self._connection_string