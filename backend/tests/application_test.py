import unittest
import os
import sys

current_folder_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_folder_path+'/../')
from application import Application

class ApplicaionTest(unittest.TestCase):
    def setUp(self) -> None:
        config_initfile = os.path.join(current_folder_path, 'testconfig.ini')
        self.app = Application()
        self.app.add_config(config_initfile)
        self.app.init_db_connection()
        return super().setUp()
    
    def test_db_connection(self):
        self.assertTrue(self.app.connection is not None)

    def test_all_tables_present(self):
        orders = self.app.connection.get_data_from_table('select * from orders;')
        self.assertFalse(type(orders) is Exception)
        
        orders_to_products = self.app.connection.get_data_from_table('select * from orders_to_products;')
        self.assertFalse(type(orders_to_products) is Exception)
        
        products = self.app.connection.get_data_from_table('select * from products;')
        self.assertFalse(type(products) is Exception)

        products_categories = self.app.connection.get_data_from_table('select * from products_categories;')
        self.assertFalse(type(products_categories) is Exception)
        
        products_to_buy = self.app.connection.get_data_from_table('select * from products_to_buy;')
        self.assertFalse(type(products_to_buy) is Exception)

        users = self.app.connection.get_data_from_table('select * from users;')
        self.assertFalse(type(users) is Exception)
    
    def test_wrong_tables_and_queries(self):
        orders = self.app.connection.get_data_from_table('SELECTION * from orders;')
        print(type(orders) is Exception)
        self.assertTrue(type(orders) is Exception)

        orders = self.app.connection.get_data_from_table('select * from orders_DATA;')
        self.assertTrue(type(orders) is Exception)

        orders = self.app.connection.get_data_from_table('')
        self.assertTrue(type(orders) is Exception)

        orders = self.app.connection.get_data_from_table('delete from orderss;')
        self.assertTrue(type(orders) is Exception)

    def test_product_table_selling_column_not_null(self):
        products = self.app.connection.get_data_from_table('select * from products;')
        self.assertTrue(all([x[-1] is not None for x in products]))

    def test_flask_is_launched(self):
        self.assertTrue(self.app.flask is not None)

    def tearDown(self) -> None:
        # close db connection
        self.app.connection.db.dispose()
        return super().tearDown()
    
if __name__ == '__main__':
    unittest.main()