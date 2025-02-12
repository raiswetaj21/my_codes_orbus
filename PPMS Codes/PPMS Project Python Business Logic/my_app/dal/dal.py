# Data Access Layer (DAL)
# Create a data access layer that handles all database operations.

class DataAccessLayer:
    def __init__(self, connection):
        self.connection = connection

    def fetch_all(self, query, params=None):
        cursor = self.connection.cursor()
        cursor.execute(query, params or ())
        return cursor.fetchall()

    def execute_query(self, query, params=None):
        cursor = self.connection.cursor()
        cursor.execute(query, params or ())
        self.connection.commit()

    # Add additional methods in future for data manipulation here

