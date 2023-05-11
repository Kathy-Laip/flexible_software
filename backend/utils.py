import numpy as np

class Connection:
    def __init__(self, db):
        self.db = db

    def get_data_from_table(self, query) -> np.ndarray or Exception:
        result = None
        try:
            connection = self.db.connect()
            result = np.array(connection.execute(query).fetchall())
            connection.close()
        except:
            result = Exception("query is failed")
        return result

    def execute_query(self, query):
        try:
            connection = self.db.connect()
            connection.execute(query)
            connection.close()
        except:
            pass
