import smtplib
import pandas as pd
import pyodbc

# Database connection details
db_host = '3.6.47.39'
db_user = 'webadmin'
db_password = 'Admin@123!@#'
db_name = 'SWMsystem'

# SQL query
sql_query = "SELECT * FROM ZoneMaster"

# Create a connection string for pyodbc
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={db_host};DATABASE={db_name};UID={db_user};PWD={db_password}'

# Connect to the database and retrieve data
connection = pyodbc.connect(connection_string)
dataframe = pd.read_sql(sql_query, connection)
connection.close()

# Convert dataframe to string
dataframe_string = dataframe.to_string(index=False)

# Email details
sender_email = input("Sender Email Address: ")
receiver_email = input("Receiver Email Address: ")

# Static subject and message
subject = "Escalation Email from SCS"
message = dataframe_string

# Combine subject and message
full_message = f"Subject: {subject}\n\n{message}"

# Set up the email server
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()

# Log in to the email account
server.login(sender_email, "mjly jzhz vadw lwrd")

# Send the email
server.sendmail(sender_email, receiver_email, full_message)

print("Email has been sent to " + receiver_email)

# Close the connection to the email server
server.quit()