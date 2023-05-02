from flask import Flask
from config import Config
from utils import Connection
import sqlalchemy

import configparser

class Application:
    def __init__(self, application_name=__name__) -> None:
        self.flask = Flask(application_name, template_folder='../pages', static_folder='../pages')
        self._config = None
        self.connection = None

    def add_config(self, config_filepath: str) -> None:
        parser = configparser.ConfigParser()
        try:
            parser.read(config_filepath)
        except:
            print("Configuration cannot be read. Invalid path provided")
            return
        
        self._config = Config()
        self._config.from_config_object(parser)

        if self.flask is not None:
            self.flask.config.from_object(self._config)
        else:
            print("Exception occured: application is not initialized. Configuration is not set")

    def init_db_connection(self):
        if self._config is None:
            print("Exception occured: configuration is not set. Database connection is not established")
        else:
            database = sqlalchemy.create_engine(self._config.SQLALCHEMY_DATABASE_URI)
            self.connection = Connection(database)