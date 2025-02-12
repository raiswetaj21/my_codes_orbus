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

# Create a connection string for pyodbc
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={db_host};DATABASE={db_name};UID={db_user};PWD={db_password}'

# Connect to the database
connection = pyodbc.connect(connection_string)


# Fetch ward names from the database
ward_query = "SELECT DISTINCT WARD FROM DP_SWEEPER_ATT_BASE_2 WHERE WARD NOT IN ('DEFAULT', 'NA', 'TFA_Ward', 'Wagholi')"
ward_df = pd.read_sql(ward_query, connection)

# Convert the ward names to a list
ward_names = ward_df['WARD'].tolist()


# Common part of the SQL query selecting 20 records
common_query_part = """
SELECT TOP 10 SWEEPERNAM, KOTHI, ATTENDANCE, IN_TIME, OUT_TIME, ROUTE_DIST, COVERED_DIST
FROM DP_SWEEPER_ATT_BASE_2
WHERE CAST(DATE_CLEAN_NEW AS DATE) = CAST(GETDATE() AS DATE)
  AND WARD = '{}'
  AND SW_BEAT_COV NOT IN ('ROUTE NOT ASSIGN')
  AND ROUTE_DIST != 0
  AND ATTENDANCE IN ('ABSENT', 'PRESENT', 'PING')
  AND COVERED_DIST <= 0.5 * ROUTE_DIST
ORDER BY SWEEPERNAM ASC
"""

# SQL queries for each ward
ward_specific_queries = {ward: common_query_part.format(ward) for ward in ward_names}

# Common part of the detailed SQL query selecting all records
common_detailed_query_part = """
SELECT SWEEPERNAM, KOTHI, ATTENDANCE, IN_TIME, OUT_TIME, ROUTE_DIST, COVERED_DIST
FROM DP_SWEEPER_ATT_BASE_2
WHERE CAST(DATE_CLEAN_NEW AS DATE) = CAST(GETDATE() AS DATE)
  AND WARD = '{}'
  AND SW_BEAT_COV NOT IN ('ROUTE NOT ASSIGN')
  AND ROUTE_DIST != 0
  AND ATTENDANCE IN ('ABSENT', 'PRESENT', 'PING')
  AND COVERED_DIST <= 0.5 * ROUTE_DIST
ORDER BY SWEEPERNAM ASC
"""

# Detailed SQL queries for Excel attachments
detailed_ward_queries = {ward: common_detailed_query_part.format(ward) for ward in ward_names}

# Email details
sender_email = "sweta.rai@scstechindia.com"
sender_password = "mjly jzhz vadw lwrd"

# Receiver emails mapped to specific wards
ward_email_map = {
    'AundhBaner': ['aditya.talegaonkar@scstechindia.com'],
    'Bhawani Peth': ['aditya.talegaonkar@scstechindia.com'],
    'Bibwewadi': ['aditya.talegaonkar@scstechindia.com'],
    'Dhankawadi-Sahakarnagar': ['divyang.patel@scstechindia.com'],
    'Dhole Patil Road': ['divyang.patel@scstechindia.com'],
    'Hadapsar-Mundhawa': ['divyang.patel@scstechindia.com'],
    'Kasba-Vishrambagwada': ['jyothy.nair@scstechindia.com'],
    'Kondhwa-Yewalewadi': ['jyothy.nair@scstechindia.com'],
    'Kothrud-Bawdhan': ['jyothy.nair@scstechindia.com'],
    'Nagar Road - Wadgaon Sheri': ['shailesh.jaiswar@scstechindia.com'],
    'Shivajinagar-Ghole Road': ['shailesh.jaiswar@scstechindia.com'],
    'Sinhgad Road': ['shailesh.jaiswar@scstechindia.com'],
    'Wanawadi-Ramtekdi': ['yashvi.bhansali@scstechindia.com'],
    'Warje-Karvenagar': ['yashvi.bhansali@scstechindia.com'],
    'Yerawada - Kalas - Dhanori': ['yashvi.bhansali@scstechindia.com']
}


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

# Iterate over each ward name and send emails
for ward in ward_names:
    # Generate SQL query for the ward
    ward_query = ward_specific_queries[ward]
    
    # Generate detailed SQL query for the ward
    detailed_ward_query = detailed_ward_queries[ward]
    
    # Generate the HTML dataframe for the email
    dataframe = pd.read_sql(ward_query, connection)
    dataframe_html = dataframe_to_html(dataframe)
    
    # Generate the detailed dataframe for the Excel attachment
    detailed_dataframe = pd.read_sql(detailed_ward_query, connection)
    excel_path = f"{ward}_details.xlsx"
    detailed_dataframe.to_excel(excel_path, index=False)
    
    # Prepare the email content
    subject = f"Daily Sweeper Report Email from SCS for {ward}"
    message = f"""
    <html>
    <body>
    <p>Dear Recipient,</p>
    <p>Please find alphabetically arranged bottom 10 sweeper details from {ward} and a detailed spreadsheet of below 50% cover distance in the attachment:</p>
    {dataframe_html}
    <p>Best regards,<br>SCS Team
    </body>
    </html>
    """
    
    # Send the email with the attachment
    send_email(sender_email, sender_password, ward_email_map[ward], subject, message, excel_path)

print("Emails have been sent successfully")

# Close the connection to the database
connection.close()