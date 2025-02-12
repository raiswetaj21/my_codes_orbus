import smtplib
import pandas as pd
import pyodbc
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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

# Convert dataframe to HTML with inline CSS
dataframe_html = dataframe.to_html(index=False, justify='left', border=1, classes='dataframe')

# Inline CSS for the table
table_style = """
<style type="text/css">
table.dataframe {
    width: 100%;
    border-collapse: collapse;
    border: 1px solid black;
    font-family: Arial, sans-serif;
    font-size: 14px;
}
table.dataframe th, table.dataframe td {
    border: 1px solid black;
    padding: 8px;
    text-align: left;
}
table.dataframe th {
    background-color: #f2f2f2;
}
</style>
"""

# Email details
sender_email = input("Sender Email Address: ")
receiver_email = input("Receiver Email Address: ")

# Static subject and message
subject = "Escalation Email from SCS"
message = f"""
<html>
<head>{table_style}</head>
<body>
<p>Dear Recipient,</p>
<p>Please find below the details from the ZoneMaster table:</p>
{dataframe_html}
<p>Best regards,<br>SCS Team</p>
</body>
</html>
"""

# Create a MIME multipart message
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = subject

# Attach the HTML message
msg.attach(MIMEText(message, 'html'))

# Set up the email server
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()

# Log in to the email account
server.login(sender_email, "mjly jzhz vadw lwrd")

# Send the email
server.sendmail(sender_email, receiver_email, msg.as_string())

print("Email has been sent to " + receiver_email)

# Close the connection to the email server
server.quit()