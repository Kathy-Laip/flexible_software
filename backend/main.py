from flask import Flask, request
import sqlalchemy
from config import Config
import numpy as np

class Connection:
    def __init__(self, db):
        self.db = db
    
    def get_data_from_table(self, query):
        connection = self.db.connect()
        return np.array(connection.execute(query).fetchall())

    def execute_query(self, query):
        connection = self.db.connect()
        connection.execute(query)

app = Flask(__name__)
app.config.from_object(Config)
my_db = sqlalchemy.create_engine(Config.SQLALCHEMY_DATABASE_URI)
connection = Connection(my_db)

print(connection.get_data_from_table('select * from clients;'))