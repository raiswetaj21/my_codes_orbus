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
ward_query = "select DISTINCT WARD from AT_COLLECTION_WORKER_ATT_BASE_2"
ward_df = pd.read_sql(ward_query, connection)

# Convert the ward names to a list
ward_names = ward_df['WARD'].tolist()

# Common part of the SQL query selecting 20 records
common_query_part = """
SELECT WARD, COUNT(*) as Total_Absent_Count 
FROM AT_COLLECTION_WORKER_ATT_BASE_2
WHERE ATTENDANCE = 'ABSENT'
AND WARD = '{}'
AND DATE_CLEAN_NEW = CONVERT(date, GETDATE())
GROUP BY WARD
"""

# SQL queries for each ward
ward_specific_queries = {ward: common_query_part.format(ward) for ward in ward_names}

# Common part of the detailed SQL query selecting all records
common_detailed_query_part = """
SELECT DATE_CLEAN_NEW, Collection_worker_name, WARD, PRABHAG, ATTENDANCE
FROM AT_COLLECTION_WORKER_ATT_BASE_2
WHERE ATTENDANCE = 'ABSENT'
AND WARD = '{}'
AND DATE_CLEAN_NEW = CONVERT(date, GETDATE())
"""

# Detailed SQL queries for Excel attachments
detailed_ward_queries = {ward: common_detailed_query_part.format(ward) for ward in ward_names}

# Email details
sender_email = "info@scstechindia.com"
sender_password = "Super123$%"

# Receiver emails mapped to specific wards
ward_email_map = {
    'AundhBaner': ['aundh@punecorporation.org'],
    'Bhawani Peth': ['asmita27284@gmail.com'],
    'Bibwewadi': ['bibwewadi@punecorporation.org'],
    'Dhankawadi-Sahakarnagar': ['dhankawadi@punecorporation.org'],
    'Dhole Patil Road': ['indrayani.deepak.gaikwad@gmail.com'],
    'Hadapsar-Mundhawa': ['hadapsar@punecorporation.org'],
    'Kasba-Vishrambagwada': ['amol.pawar34@gmail.com'],
    'Kondhwa-Yewalewadi': ['hkirulkar001@gmail.com'],
    'Kothrud-Bawdhan': ['kothrud@punecorporation.org'],
    'Nagar Road - Wadgaon Sheri': ['somnath.bankar@punecorporation.org'],
    'Shivajinagar-Ghole Road': ['gwo@punecorporation.org'],
    'Sinhgad Road': ['sandip.khalate@punecorporation.org'],
    'Wanawadi-Ramtekdi': ['wanawadi@punecorporation.org'],
    'Warje-Karvenagar': ['warjekarvenagar@punecorporation.org'],
    'Yerawada - Kalas - Dhanori': ['city1nagtilak69@gmail.com']
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
    excel_path = f"{ward}_collectionworkerdetails.xlsx"
    detailed_dataframe.to_excel(excel_path, index=False)
    
    # Get current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Prepare the email content
    zone_number = ward_zone_map.get(ward, 'Unknown')
    subject = f"Collection Worker Report Email from SCS for {ward} (Zone {zone_number}) at {current_time}"
    message = f"""
    <html>
    <body>
    <p>Dear Recipient,</p>
    <p>Please find the total absent count from {ward} (Zone {zone_number}) and a detailed spreadsheet of absent collection workers in the attachment:</p>
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