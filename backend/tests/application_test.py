import unittest
from application import Application
import os

class ApplicaionTest(unittest.TestCase):
    def setUp(self) -> None:
        current_folder_path = os.path.dirname(os.path.abspath(__file__))
        config_initfile = os.path.join(current_folder_path, 'testconfig.ini')
        self.app = Application()
        self.app.add_config(config_initfile)
        self.app.init_db_connection()
        return super().setUp()
    
    def test_db_connection(self):
        pass

    def test_product_table_selling_column_not_null(self):
        pass

    def test_flask_is_launched(self):
        pass

    def tearDown(self) -> None:
        # close db connection
        return super().tearDown()