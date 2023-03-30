from flask import Flask, request, render_template
import sqlalchemy
from config import Config
import numpy as np
import json
import os

class Connection:
    def __init__(self, db):
        self.db = db
    
    def get_data_from_table(self, query):
        connection = self.db.connect()
        return np.array(connection.execute(query).fetchall())

    def execute_query(self, query):
        connection = self.db.connect()
        connection.execute(query)

app = Flask(__name__, template_folder='../pages')
app.config.from_object(Config)
my_db = sqlalchemy.create_engine(Config.SQLALCHEMY_DATABASE_URI)
connection = Connection(my_db)

@app.route("/signin'", methods=["POST"])
def signInUser():
    sign_in_info = json.loads(request.get_data())
    login = sign_in_info['login']
    password = sign_in_info['password']

    if login == '' or password == '' or login is None or password is None:
        return r'{otvet:"False"}'

    data = connection.get_data_from_table(f"select status from users where login='{login}' and password='{password}'")
    print(data)

    if len(data) == 0:
        return r'{otvet: "False"}'
    
    return json.dumps({'otvet': True, 'status': data[0][0]})

@app.route("/pages/index.html", methods=["GET", "POST"])
def index():
    print(os.getcwd())
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")