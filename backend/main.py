from flask import Flask, request, render_template
import sqlalchemy
from config import Config
import numpy as np
import json

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

@app.route("/getServicesOnManager", methods=["POST"])
def getServicesOnManager():
    product_type = 'услуга'
    
    products = connection.get_data_from_table(f'''select prod.id, prod.cost_for_one, prod.details, cat.name from products as prod
        JOIN products_categories as cat
        on cat.id = prod.category
        where prod.type=\'{product_type}\';''')
    
    if len(products) == 0:
        return r'{"services": []}'
    
    products_response = {"services": []}

    for product in products:
        products_response['services'].append({
            "id": int(product[0]),
            "cost": int(product[1]),
            "description": product[2],
            "type": product[3]
        })

    return json.dumps(products_response)

@app.route("/getStuffOnManager", methods=["POST"])
def getStuffOnManager():

    products = connection.get_data_from_table(f'''select prod.id, prod.cost_for_one, prod.details, cat.name from products as prod
        JOIN products_categories as cat
        on cat.id = prod.category;''')

    if len(products) == 0:
        return r'{"stuff": \[], "category": \[]}'

    products_response = {"stuff": [], 'category': []}
    unique_types = set()

    for product in products:
        products_response['stuff'].append({
            "id": int(product[0]),
            "cost": int(product[1]),
            "description": product[2],
            "type": product[3]
        })

        if product[3] not in unique_types:
            products_response['category'].append({
                'type': product[3]
            })
        
        unique_types.add(product[3])

    return json.dumps(products_response)

@app.route("/getOrders", methods=["POST"])
def getOrders():
    client_id = json.loads(request.get_data())

    orders = connection.get_data_from_table(f'''select "id", "price", "status", "address", "deadmans_name" from "orders" where "client_ID"={client_id};''')

    if orders is None or len(orders) == 0:
        return json.dumps(r'{orders: []}')
    
    orders_response = {"orders": []}
    for order in orders:
        orders_response['orders'].append({
            'id': order[0],
            'price': order[1],
            'status': order[2],
            'address': order[3],
            'deadmans_name': order[4]
        })

    return json.dumps(orders_response)

@app.route("/getOrdersByManager", methods=["POST"])
def getOrdersByManager():
    manager = json.loads(request.get_data())

    bd_request = '''select "id", "price", "status", "address", "deadmans_name" from "orders"''' +\
        (f''' where "manager_ID"={manager['id']};''' if not manager['all'] else ';')

    orders = connection.get_data_from_table(bd_request)

    if orders is None or len(orders) == 0:
        return json.dumps(r'{orders: []}')
    
    orders_response = {"orders": []}
    for order in orders:
        orders_response['orders'].append({
            'id': order[0],
            'price': order[1],
            'status': order[2],
            'address': order[3],
            'deadmans_name': order[4]
        })

    return json.dumps(orders_response)

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port="5050")