from configparser import ConfigParser

class Config:
    def __init__(self) -> None:
        self.username = None
        self.password = None
        self.SQLALCHEMY_DATABASE_URI = None
        self.SQLALCHEMY_TRACK_MODIFICATIONS = None
        self.CSRF_ENABLED = None
        self.SECRET_KEY = None

    def from_config_object(self, config: ConfigParser) -> None:
        self.username = config.get('flask_config', 'username')
        self.password = config.get('flask_config', 'password')
        self.SQLALCHEMY_DATABASE_URI = config.get('flask_config', 'SQLALCHEMY_DATABASE_URI')
        self.SQLALCHEMY_TRACK_MODIFICATIONS = config.get('flask_config', 'SQLALCHEMY_TRACK_MODIFICATIONS')
        self.CSRF_ENABLED = config.get('flask_config', 'CSRF_ENABLED')
        self.SECRET_KEY = config.get('flask_config', 'SECRET_KEY')
        print('Exception occured when parsing config from dictionary')