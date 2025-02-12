import pyodbc
import numpy as np
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

today = datetime.date.today() # Captures current date

# Database connection details
db_host = '3.6.47.39'
db_user = 'webadmin'
db_password = 'Admin@123!@#'
db_name = 'SWMsystem'

# Create a connection string for pyodbc
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={db_host};DATABASE={db_name};UID={db_user};PWD={db_password}'

# Establish the connection
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

# Connect to the database
try:
    connection = pyodbc.connect(connection_string)
except Exception as e:
    print(f"Error connecting to the database: {e}")
    exit()

cursor.execute("exec proc_MainDashboard_python @mode = ?, @accid = ?, @startdate= ?, @enddate=?",
                   (25,11401,today,today))

data_frames = []

while True:
    # Check if there are any results to fetch
    if cursor.description is not None:
        col_names = [x[0] for x in cursor.description]
        data = [tuple(x) for x in cursor.fetchall()]  # Convert pyodbc.Row objects to tuples
        data_frames.append(pd.DataFrame(data, columns=col_names))

    # Move to the next result set
    if not cursor.nextset():
        break

# Access each dataframe
if data_frames:
    data_mechsweeper = data_frames[1]  # Since the second DataFrame is for the 'mechanical sweeper' single record result set
else:
    data_mechsweeper = None  # If no result sets, set data_mechsweeper to None

# Email configuration
subject = f"Mechanical Sweeper Data Issue Detected on {today}"
to_emails = ['aditya.talegaonkar@scstechindia.com', 'divyang.patel@scstechindia.com', 'jahangir.navlekar@scstechindia.com',
             'joylin.bosco@scstechindia.com', 'jyothy.nair@scstechindia.com', 'rakeshjain@scstechindia.com',
             'shailesh.jaiswar@scstechindia.com', 'trushna.ghogale@scstechindia.com', 'yashvi.bhansali@scstechindia.com',
             'yashwant.pangam@scstechindia.com', 'vikram.dhole@scstechindia.com', 'hariprasad.dandime@scstechindia.com',
             'ajay.kedar@scstechindia.com', 'yogesh.pawar@scstechindia.com', 'hemant.wani@scstechindia.com', 'sweta.rai@scstechindia.com']
from_email = "info@scstechindia.com"
smtp_server = 'smtp.gmail.com'
smtp_port = 587  # Typically 587 is for TLS
login = "info@scstechindia.com"
password = "Super123$%"

# Function to convert DataFrame to HTML
def dataframe_to_html(data_mechsweeper):
    # Convert DataFrame to HTML
    dataframe_html = data_mechsweeper.to_html(index=False, justify='left', border=1, classes='dataframe')
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

# Function to send email
def send_email(subject, body, to_emails, from_email, smtp_server, smtp_port, login, password):
    # Create a multipart message and set headers
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ", ".join(to_emails)
    msg['Subject'] = subject

    # Add body to email
    msg.attach(MIMEText(body, 'html'))

    # Connect to the server and send the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(login, password)
        server.sendmail(from_email, to_emails, msg.as_string())
        server.quit()
        print("Emails sent successfully!")
    except Exception as e:
        print(f"Failed to send emails: {e}")

# Check for zero values in specified columns
if (data_mechsweeper[['Cover', 'UnCover', 'PartiallyCover']] == 0).any(axis=None):
    html_table = dataframe_to_html(data_mechsweeper)
    email_body = f"""
    <html>
    <body>
    <p>Dear Recipient,</p>
    <p>Found Data Issue in Mechanical Sweeper: One or more of the columns Cover, UnCover or PartiallyCover has a value of 0. Below are the details:</p>{html_table}
    <p>Best regards,<br>SCS Team</p>
    <p style="color: gray; font-size: 12px;">This is an auto-generated email, please do not reply.</p>
    </body>
    </html>
    """
    send_email(subject, email_body, to_emails, from_email, smtp_server, smtp_port, login, password)
else:
    print("No issues in data.")