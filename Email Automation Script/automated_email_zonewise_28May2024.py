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

# SQL queries for each zone
zone_queries = {
    "zone1": "select top 10 * from tblzone1",
    "zone2": "select top 10 * from tblzone2",
    "zone3": "select top 10 * from tblzone3",
    "zone4": "select top 10 * from tblzone4",
    "zone5": "select top 10 * from tblzone5"
}

# Email details
sender_email = "sweta.rai@scstechindia.com"
sender_password = "mjly jzhz vadw lwrd"

# Receiver emails mapped to specific zones
zone_email_map = {
    "zone1": ["aditya.talegaonkar@scstechindia.com"],
    "zone2": ["divyang.patel@scstechindia.com"],
    "zone3": ["jyothy.nair@scstechindia.com"],
    "zone4": ["shailesh.jaiswar@scstechindia.com"],
    "zone5": ["yashvi.bhansali@scstechindia.com"]
}

# Create a connection string for pyodbc
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={db_host};DATABASE={db_name};UID={db_user};PWD={db_password}'

# Connect to the database
connection = pyodbc.connect(connection_string)

# Function to convert dataframe to HTML with inline CSS
def dataframe_to_html(df):
    dataframe_html = df.to_html(index=False, justify='left', border=1, classes='dataframe')
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
    return f"<html><head>{table_style}</head><body>{dataframe_html}</body></html>"

# Email sending function
def send_email(sender_email, sender_password, receiver_email, subject, message):
    # Create a MIME multipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(receiver_email)
    msg['Subject'] = subject

    # Attach the HTML message
    msg.attach(MIMEText(message, 'html'))

    # Set up the email server
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    # Log in to the email account
    server.login(sender_email, sender_password)

    # Send the email
    server.sendmail(sender_email, receiver_email, msg.as_string())

    # Close the connection to the email server
    server.quit()

# Iterate over each zone query and send emails
for zone, query in zone_queries.items():
    dataframe = pd.read_sql(query, connection)
    dataframe_html = dataframe_to_html(dataframe)
    subject = f"Escalation Email from SCS - {zone}"
    message = f"""
    <html>
    <body>
    <p>Dear Recipient,</p>
    <p>Please find below the details from the {zone} table:</p>
    {dataframe_html}
    <p>Best regards,<br>SCS Team</p>
    </body>
    </html>
    """
    send_email(sender_email, sender_password, zone_email_map[zone], subject, message)

print("Emails have been sent successfully")

# Close the connection to the database
connection.close()
