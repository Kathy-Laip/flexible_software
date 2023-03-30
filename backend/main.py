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

app = Flask(__name__, template_folder='../pages', static_folder='../pages')
app.config.from_object(Config)
my_db = sqlalchemy.create_engine(Config.SQLALCHEMY_DATABASE_URI)
connection = Connection(my_db)

@app.route("/signin", methods=["POST"])
def signInUser():
    sign_in_info = json.loads(request.get_data())
    login = sign_in_info['login']
    password = sign_in_info['password']

    if login == '' or password == '' or login is None or password is None:
        return r'{otvet:"False"}'

    data = connection.get_data_from_table(f"select id, status from users where login='{login}' and password='{password}'")

    if len(data) == 0:
        return r'{otvet: "False"}'
    
    return json.dumps({'otvet': True, 'status': data[0][1], 'id': int(data[0][0])})

@app.route("/getProductsOnManager", methods=["POST"])
def getProductsOnManager():
    product_type = 'товар'
    
    products = connection.get_data_from_table(f'''select prod.id, prod.cost_for_one, prod.details, cat.name from products as prod
        JOIN products_categories as cat
        on cat.id = prod.category
        where prod.type=\'{product_type}\';''')
    
    if len(products) == 0:
        return r'{"products": []}'
    
    products_response = {"products": []}

    for product in products:
        products_response['products'].append({
            "id": int(product[0]),
            "cost": int(product[1]),
            "description": product[2],
            "type": product[3]
        })

    return json.dumps(products_response)

# pages
@app.route("/pages/index.html", methods=["GET"])
def index():
    return render_template('index.html')

@app.route("/pages/managerStorage.html", methods=["GET"])
def managerStorage():
    return render_template('managerStorage.html')

@app.route("/pages/managerServices.html", methods=["GET"])
def managerServices():
    return render_template('managerServices.html')

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1")
