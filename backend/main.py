from flask import request
import numpy as np
import json
from application import Application
import os

current_folder_path = os.path.dirname(os.path.abspath(__file__))
initfile = os.path.join(current_folder_path, 'config.ini')

app = Application()
app.add_config(initfile)
app.init_db_connection()

@app.flask.route("/signin", methods=["POST"])
def signInUser():
    sign_in_info = json.loads(request.get_data())
    login = sign_in_info['login']
    password = sign_in_info['password']

    if login == '' or password == '' or login is None or password is None:
        return r'{otvet:"False"}'

    data = app.connection.get_data_from_table(f"select id, status from users where login='{login}' and password='{password}'")

    if len(data) == 0:
        return r'{otvet: "False"}'
    
    return json.dumps({'otvet': True, 'status': data[0][1], 'id': int(data[0][0])})

@app.flask.route("/getProductsOnManager", methods=["POST"])
def getProductsOnManager():
    product_type = 'товар'
    
    products = app.connection.get_data_from_table(f'''select prod.id, prod.cost_for_one, prod.details, cat.name from products as prod
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

@app.flask.route("/getServicesOnManager", methods=["POST"])
def getServicesOnManager():
    product_type = 'услуга'
    
    products = app.connection.get_data_from_table(f'''select prod.id, prod.cost_for_one, prod.details, cat.name from products as prod
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

@app.flask.route("/getStuffOnManager", methods=["POST"])
def getStuffOnManager():

    products = app.connection.get_data_from_table(f'''select prod.id, prod.cost_for_one, prod.details, cat.name from products as prod
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

@app.flask.route("/getOrders", methods=["POST"])
def getOrders():
    client_id = json.loads(request.get_data())

    orders = app.connection.get_data_from_table(f'''select "id", "price", "status", "address", "deadmans_name" from "orders" where "client_ID"={client_id};''')

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

@app.flask.route("/getOrdersByManager", methods=["POST"])
def getOrdersByManager():
    manager = json.loads(request.get_data())

    bd_request = '''select "id", "price", "status", "address", "deadmans_name" from "orders"''' +\
        (f''' where "manager_ID"={manager['id']};''' if not manager['all'] else ';')

    orders = app.connection.get_data_from_table(bd_request)

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

@app.flask.route("/addEstimate", methods=["POST"])
def addEstimate():
    estimate = json.loads(request.get_data())
    info = estimate['info']
    products = estimate['products']
    print(info, products)

    price = 0
    for product in products:
        price += product['pr']

    select_client_ID_by_phone_request = f'''select id from "users" where "phone"='{info["phoneNumberClient"]}';'''
    client_id = app.connection.get_data_from_table(select_client_ID_by_phone_request)[0][0]

    add_order_query = f'''insert into "orders"("client_ID", "manager_ID", "price", "status", "address", "deadmans_name", "deadmans_passport")
        values ({client_id}, {info["manageriD"]}, {price}, '{"Оформлено"}', '{info["address"]}', '{info["nameDeceased"]}', '{info["dataPassport"]}');'''
    
    app.connection.execute_query(add_order_query)

    all_order_id_request = '''select "order_ID" from "orders_to_products";'''
    order_id = int(np.max(app.connection.get_data_from_table(all_order_id_request).flatten())+1)

    for product in products:
        product_id_request =\
        f'''
            select prod.id from "products" as prod
            join products_categories as category on prod.category=category.id
            where category.name='{product["category"]}' and prod.details='{product["details"]}';
        '''
        prod_id = app.connection.get_data_from_table(product_id_request)[0][0]

        add_new_product_query = f'''insert into "orders_to_products"("order_ID", "product_ID", "amount")
            values ({order_id}, {prod_id}, {product["count"]});'''
        
        app.connection.execute_query(add_new_product_query)
    
    return json.dumps({"response": True})

@app.flask.route("/addNewProducts", methods=["POST"])
def addNewProducts():
    products = json.loads(request.get_data())

    for product in products:
        product_id_request =\
        f'''
            select prod.id from "products" as prod
            join products_categories as category on prod.category=category.id
            where category.name='{product["category"]}' and prod.details='{product["details"]}';
        '''

        prod_id = app.connection.get_data_from_table(product_id_request)[0][0]

        add_new_product_query = f'''insert into "products_to_buy"("product_ID", "amount")
            values ({prod_id}, {product["count"]});'''
        app.connection.execute_query(add_new_product_query)
    
    return json.dumps({"response": True})

if __name__ == '__main__':
    app.flask.run(debug=True, host="127.0.0.1", port="5050")