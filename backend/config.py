class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://admin:lolkekcheburek@localhost/memento_mori'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
 
    CSRF_ENABLED = True
    SECRET_KEY = 'no_time_to_die'