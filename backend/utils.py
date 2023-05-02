import numpy as np

class Connection:
    def __init__(self, db):
        self.db = db
    
    def get_data_from_table(self, query):
        result = None
        connection = self.db.connect()
        result = np.array(connection.execute(query).fetchall())
        connection.close()
        return result

    def execute_query(self, query):
        connection = self.db.connect()
        connection.execute(query)
        connection.close()
