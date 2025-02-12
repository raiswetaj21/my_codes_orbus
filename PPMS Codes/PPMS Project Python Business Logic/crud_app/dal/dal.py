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
            # Execute the insert statement
            cursor.execute(query, params)
            # Fetch the new ID
            cursor.execute("SELECT SCOPE_IDENTITY()")
            result = cursor.fetchone()
            print(f"Result value is: {result}\n")
            new_id = result[0] if result else None
            self.connection.commit()
            print(f"Inserted record ID: {new_id}\n")  # Debugging information
            return new_id
        except Exception as e:
            print(f"Error during insert_record: {e}\n")
            self.connection.rollback()
            return None
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
