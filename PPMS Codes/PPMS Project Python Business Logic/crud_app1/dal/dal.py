class DataAccessLayer:
    def __init__(self, connection):
        self.connection = connection

    def fetch_all(self, query, params=None):
        cursor = self.connection.cursor()
        cursor.execute(query, params or ())
        return cursor.fetchall()

    def fetch_one(self, query, params=None):
        cursor = self.connection.cursor()
        cursor.execute(query, params or ())
        return cursor.fetchone()

    def insert_record(self, query, params):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            self.connection.commit()
            print(f"Record inserted successfully\n")  # Debugging information
        except Exception as e:
            print(f"Error during insert_record: {e}\n")
            print(f"SQL Query: {query}\n")
            self.connection.rollback()
        finally:
            cursor.close()

    def update_record(self, query, params):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()

    def delete_record(self, query, params):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()

    def fetch_many(self, query, size, params=None):
        cursor = self.connection.cursor()
        cursor.execute(query, params or ())
        return cursor.fetchmany(size)
