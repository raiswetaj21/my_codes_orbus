import smtplib
import pandas as pd
import pyodbc
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Database connection details
db_host = '3.6.47.39'
db_user = 'webadmin'
db_password = 'Admin@123!@#'
db_name = 'SWMsystem'

# SQL queries for each zone
zone_queries = {
    "zone1": "SELECT TOP 10 * FROM tblzone1",
    "zone2": "SELECT TOP 10 * FROM tblzone2",
    "zone3": "SELECT TOP 10 * FROM tblzone3",
    "zone4": "SELECT TOP 10 * FROM tblzone4",
    "zone5": "SELECT TOP 10 * FROM tblzone5"
}

# Detailed SQL queries for Excel attachments
detailed_zone_queries = {
    "zone1": "SELECT * FROM tblzone1",
    "zone2": "SELECT * FROM tblzone2",
    "zone3": "SELECT * FROM tblzone3",
    "zone4": "SELECT * FROM tblzone4",
    "zone5": "SELECT * FROM tblzone5"
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

# Email sending function with attachment
def send_email(sender_email, sender_password, receiver_email, subject, message, attachment_path):
    # Create a MIME multipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(receiver_email)
    msg['Subject'] = subject

    # Attach the HTML message
    msg.attach(MIMEText(message, 'html'))

    # Attach the Excel file
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(attachment_path, 'rb').read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename="{attachment_path}"')
    msg.attach(part)

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
    # Generate the HTML dataframe for the email
    dataframe = pd.read_sql(query, connection)
    dataframe_html = dataframe_to_html(dataframe)
    
    # Generate the detailed dataframe for the Excel attachment
    detailed_query = detailed_zone_queries[zone]
    detailed_dataframe = pd.read_sql(detailed_query, connection)
    excel_path = f"{zone}_details.xlsx"
    detailed_dataframe.to_excel(excel_path, index=False)
    
    # Prepare the email content
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
    
    # Send the email with the attachment
    send_email(sender_email, sender_password, zone_email_map[zone], subject, message, excel_path)

print("Emails have been sent successfully")

# Close the connection to the database
connection.close()
