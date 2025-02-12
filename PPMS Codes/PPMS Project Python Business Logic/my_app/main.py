# Application Layer
# This is where your application interacts with the business logic layer.
# It could be a web application, command-line tool, or any other interface.

from business_logic.business_logic import BusinessLogic
from dal.dal import DataAccessLayer
from db_config.db_config import get_db_connection

try:
    print("Establishing database connection...")
    conn = get_db_connection()
    print("Database connection established")
    print("Initializing Data Access Layer...")
    dal = DataAccessLayer(conn)
    print("Data Access Layer initialized")
    print("Initializing Business Logic...")
    bl = BusinessLogic(dal)
    print("Business Logic initialized")
except Exception as e:
    print(f"Error during initialization: {e}")

if __name__ == "__main__":
    # Create a new user
    # bl.create_user({'name': 'John Doe', 'email': 'john@example.com'})

    # Fetch and print all existing users
    users = bl.get_users()
    print("Datatype of users variable is",type(users))
    for user in users:
        print(user)
