class BusinessLogic:
    def __init__(self, dal):
        self.dal = dal

    def get_users(self):
        query = "SELECT * FROM Users"
        return self.dal.fetch_all(query)

    def get_user_by_id(self, user_id):
        query = "SELECT * FROM Users WHERE UserID = ?"
        return self.dal.fetch_one(query, (user_id,))

    def create_user(self, user_data):
        # Get the current max UserID
        max_user_id = self.dal.fetch_one("SELECT MAX(UserID) FROM Users")[0]
        new_user_id = max_user_id + 1 if max_user_id is not None else 1
        user_data['UserID'] = new_user_id
        query = """
        INSERT INTO Users (UserID, Name, ProjectName, ContactPerson, ContactEmail, ContactNo, Location)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        self.dal.insert_record(query, (user_data['UserID'], user_data['Name'], user_data['ProjectName'],
                                              user_data['ContactPerson'], user_data['ContactEmail'],
                                              user_data['ContactNo'], user_data['Location']))
        return new_user_id

    def update_user_email(self, user_id, new_email):
        query = "UPDATE Users SET ContactEmail = ? WHERE UserID = ?"
        self.dal.update_record(query, (new_email, user_id))

    def delete_user(self, user_id):
        query = "DELETE FROM Users WHERE UserID = ?"
        self.dal.delete_record(query, (user_id,))
