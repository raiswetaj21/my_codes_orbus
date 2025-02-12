from business_logic.business_logic import BusinessLogic
from dal.dal import DataAccessLayer
from db_config.db_config import get_db_connection

# Establish the database connection
conn = get_db_connection()

# Initialize Data Access Layer and Business Logic
dal = DataAccessLayer(conn)
bl = BusinessLogic(dal)

if __name__ == "__main__":
    # Fetch and print all existing users
    users = bl.get_users()
    print("Printing all records in Users table...")
    for user in users:
        print(user)
    print("\n")

    # Create a new user and print the new user's ID
    user_data = {'UserID': 21, 'Name': 'Jane Doe', 'ProjectName': 'Project Phi',
                                  'ContactPerson': 'Olive Smith', 'ContactEmail': 'jane.doh@example.com',
                                  'ContactNo': '123-456-7910', 'Location': 'Manhattan'}
    new_user_id = bl.create_user(user_data)
    if new_user_id is not None:
        print(f"Created new user with ID: {new_user_id}\n")
    else:
        print("Record being pulled is None.\n")

    # Update a user's email
    bl.update_user_email(new_user_id, 'jane.doe@example.com')
    print(f"Updated user {new_user_id}'s email to jane.doe@example.com\n")

    # Fetch and print a single user by ID
    user = bl.get_user_by_id(21)
    print("Printing the new user...")
    print(user)
    print("\n")

    # Delete a user
    bl.delete_user(new_user_id)
    print(f"Deleted user with ID {new_user_id}")
