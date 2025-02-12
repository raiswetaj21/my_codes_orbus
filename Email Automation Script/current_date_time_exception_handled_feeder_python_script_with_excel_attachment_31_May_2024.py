import smtplib
import pandas as pd
import pyodbc
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

# Database connection details
db_host = '3.6.47.39'
db_user = 'webadmin'
db_password = 'Admin@123!@#'
db_name = 'SWMsystem'

# Create a connection string for pyodbc
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={db_host};DATABASE={db_name};UID={db_user};PWD={db_password}'

# Connect to the database
try:
    connection = pyodbc.connect(connection_string)
except Exception as e:
    print(f"Error connecting to the database: {e}")
    exit()

# Fetch ward names from the database
ward_query = "SELECT DISTINCT WARD FROM DP_SWEEPER_ATT_BASE_2 WHERE WARD NOT IN ('DEFAULT', 'NA', 'TFA_Ward', 'Wagholi')"
ward_df = pd.read_sql(ward_query, connection)

# Convert the ward names to a list
ward_names = ward_df['WARD'].tolist()

# Common part of the SQL query selecting 20 records
common_query_part = """
SELECT TOP 10 Vehiclename as 'Vehicle Name', WARD as Ward, FEEDERNAME as 'Feeder Name', STATUS as Status, First_Intersection_Time as 'First Intersection Time', Last_Intersection_Time as 'Last Intersection Time', EXPECTEDTIME as 'Expected Time'
FROM FEEDER_BASE_DP_AT
WHERE CAST(DATE_CLEAN_NEW AS DATE) = CAST(GETDATE() AS DATE)
AND WARD = '{}'
AND STATUS != 'COVERED'
AND EXPECTEDTIME IS NOT NULL
AND EXPECTEDTIME != ''
ORDER BY STATUS DESC
"""

# SQL queries for each ward
ward_specific_queries = {ward: common_query_part.format(ward) for ward in ward_names}

# Common part of the detailed SQL query selecting all records
common_detailed_query_part = """
SELECT Vehiclename as 'Vehicle Name', WARD as Ward, FEEDERNAME as 'Feeder Name', STATUS as Status, First_Intersection_Time as 'First Intersection Time', Last_Intersection_Time as 'Last Intersection Time', EXPECTEDTIME as 'Expected Time'
FROM FEEDER_BASE_DP_AT
WHERE CAST(DATE_CLEAN_NEW AS DATE) = CAST(GETDATE() AS DATE)
AND WARD = '{}'
AND STATUS != 'COVERED'
AND EXPECTEDTIME IS NOT NULL
AND EXPECTEDTIME != ''
ORDER BY STATUS DESC
"""

# Detailed SQL queries for Excel attachments
detailed_ward_queries = {ward: common_detailed_query_part.format(ward) for ward in ward_names}

# Email details
sender_email = "sweta.rai@scstechindia.com"
sender_password = "mjly jzhz vadw lwrd"

# Receiver emails mapped to specific wards
ward_email_map = {
    'AundhBaner': ['aundhhealthdept@gmail.com', 'nikamnikhil0@gmail.com'],
    'Bhawani Peth': ['aditya.talegaonkar@scstechindia.com'],
    'Bibwewadi': ['jahangir.navlekar@scstechindia.com'],
    'Dhankawadi-Sahakarnagar': ['divyang.patel@scstechindia.com'],
    'Dhole Patil Road': ['pratik.ghosh@scstechindia.com'],
    'Hadapsar-Mundhawa': ['joylin.bosco@scstechindia.com'],
    'Kasba-Vishrambagwada': ['jyothy.nair@scstechindia.com'],
    'Kondhwa-Yewalewadi': ['jyothy.nair@scstechindia.com'],
    'Kothrud-Bawdhan': ['rakeshjain@scstechindia.com'],
    'Nagar Road - Wadgaon Sheri': ['shailesh.jaiswar@scstechindia.com'],
    'Shivajinagar-Ghole Road': ['shailesh.jaiswar@scstechindia.com'],
    'Sinhgad Road': ['trushna.ghogale@scstechindia.com'],
    'Wanawadi-Ramtekdi': ['yashvi.bhansali@scstechindia.com'],
    'Warje-Karvenagar': ['yashvi.bhansali@scstechindia.com'],
    'Yerawada - Kalas - Dhanori': ['yashwant.pangam@scstechindia.com']
}

# Zone numbers mapped to specific wards
ward_zone_map = {
    'AundhBaner': 2,
    'Bhawani Peth': 5,
    'Bibwewadi': 5,
    'Dhankawadi-Sahakarnagar': 3,
    'Dhole Patil Road': 1,
    'Hadapsar-Mundhawa': 4,
    'Kasba-Vishrambagwada': 5,
    'Kondhwa-Yewalewadi': 4,
    'Kothrud-Bawdhan': 2,
    'Nagar Road - Wadgaon Sheri': 1,
    'Shivajinagar-Ghole Road': 2,
    'Sinhgad Road': 3,
    'Wanawadi-Ramtekdi': 4,
    'Warje-Karvenagar': 3,
    'Yerawada - Kalas - Dhanori': 1
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
    try:
        # Create a MIME multipart message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = ", ".join(receiver_email)
        msg['Subject'] = subject

        # Attach the HTML message
        msg.attach(MIMEText(message, 'html'))

        # Attach the Excel file
        with open(attachment_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{attachment_path}"')
        # part.add_header('Content-Disposition', "attachment; filename= %s" % attachment_path)
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

        print(f"Email sent to {', '.join(receiver_email)} for ward {subject.split()[-1]}")
    except Exception as e:
        print(f"Failed to send email to {', '.join(receiver_email)}: {e}")

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
    excel_path = f"{ward}_feederdetails.xlsx"
    detailed_dataframe.to_excel(excel_path, index=False)
    
    # Get current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Prepare the email content
    zone_number = ward_zone_map.get(ward, 'Unknown')
    subject = f"Feeder Report Email from SCS for {ward} (Zone {zone_number}) at {current_time}"
    message = f"""
    <html>
    <body>
    <p>Dear Recipient,</p>
    <p>Please find snippet of feeder details from {ward} (Zone {zone_number}) and a detailed spreadsheet of uncovered and unattended feeder vehicles in the attachment:</p>
    {dataframe_html}
    <p>Best regards,<br>SCS Team</p>
    <p style="color: gray; font-size: 12px;">This is an auto-generated email, please do not reply.</p>
    </body>
    </html>
    """
    
    # Send the email with the attachment
    if ward in ward_email_map:
        send_email(sender_email, sender_password, ward_email_map[ward], subject, message, excel_path)
    else:
        print(f"No email mapping found for ward: {ward}")

print("All report emails have been sent successfully.")

# Close the connection to the database
connection.close()