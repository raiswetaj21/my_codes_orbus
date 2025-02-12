# Business Logic Layer
# Implement your business logic in separate classes or modules.
# This layer should interact with the DAL to fetch and manipulate data.

class BusinessLogic:
    def __init__(self, dal):
        self.dal = dal

    def get_users(self):
        query = "SELECT * FROM Users"
        return self.dal.fetch_all(query)

    # def create_user(self, user_data):
    #     query = "INSERT INTO Users (Name, Email) VALUES (?, ?)"
    #     self.dal.execute_query(query, (user_data['name'], user_data['email']))

    # Add additional business logic methods in future here

