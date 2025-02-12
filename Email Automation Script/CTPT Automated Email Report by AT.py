import smtplib
import pandas as pd
import pyodbc
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from datetime import datetime as dt
import datetime


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

# Fetch ward names from the database
ward_query = "SELECT DISTINCT WARD FROM DP_SWEEPER_ATT_BASE_2 WHERE WARD NOT IN ('DEFAULT', 'NA', 'TFA_Ward', 'Wagholi')"
ward_df = pd.read_sql(ward_query, connection)

# Convert the ward names to a list
ward_names = ward_df['WARD'].tolist()

today = datetime.date.today()
cursor.execute("exec proc_CTPTDailyChecking_DP_PYTHON @Mode = ?, @Accid = ?, @fromdate= ?, @todate=? , @zoneid = ?, @wardid =?, @blocktypeid =?, @imgId = ?, @kothiid = ?",
                   (5,11401, today,today , 0,0,0,0,0))

data_frames = []

while True:
    # Check if there are any results to fetch
    if cursor.description is not None:
        col_names = [x[0] for x in cursor.description]
        data = [tuple(x) for x in cursor.fetchall()]  # convert pyodbc.Row objects to tuples
        data_frames.append(pd.DataFrame(data, columns=col_names))

    # Move to the next result set
    if not cursor.nextset():
        break

# Access each dataframe
if data_frames:
    data_ctpt = data_frames[0]  # Assuming the first DataFrame is for the 'data_sweeper' result set
else:
    data_ctpt = None  # If no result sets, set data_sweeper to None

filtered_df = data_ctpt[data_ctpt['Status'].isin(['Unvisited', 'Invalid'])]
selected_columns = ['BlockName', 'Mokadam', 'ZoneName', 'wardName', 'KothiName', 'Date','Status']
final_filtered_df = filtered_df[selected_columns]
wardwise_groups = final_filtered_df.groupby('wardName')
top_10_wardwise = wardwise_groups.apply(lambda x: x.head(10))
top_10_wardwise = top_10_wardwise.reset_index(drop=True)

# Receiver emails mapped to specific wards
ward_email_map = {
    'AundhBaner': ['aundhhealthdept@gmail.com','nikamnikhil0@gmail.com','iswmaundhattdence1@gmail.com',
                   'saurabh.koli@scstechindia.com', 'shinnu.waghmare@scstechindia.com',
                   'mahavir.maske@scstechindia.com', 'hariprasad.dandime@scstechindia.com', 'ajay.kedar@scstechindia.com', 'yogesh.pawar@scstechindia.com'],
    'Bhawani Peth': ['bhavanipeth@punecorporation.org', 'mukhtarsayyed1@gmail.com' ,
                     'chandravadangaikwad552@gmail.com',
                     'nitinsalunke9894@gmail.com', 'nilesh10099@gmail.com', 'bagulraju49@gmail.com',
                     'govindapatole861@gmail.com', 'somnath.shinde@scstechindia.com',
                     'pramodgaikwad1973@gmail.com', 'mohanchandele92@gmail.com', 'shivjigaiakwad@gmail.com',
                     'bhushan.badgujar@scstechindia.com', 'onkar.vedpathak@scstechindia.com', 'hariprasad.dandime@scstechindia.com', 'ajay.kedar@scstechindia.com', 'yogesh.pawar@scstechindia.com'],
    'Bibwewadi': ['bibwewadi@punecorporation.org', 'sunilmohite73@gmail.com', 'omkar.lad@scstechindia.com',
                  'hariprasad.dandime@scstechindia.com', 'ajay.kedar@scstechindia.com', 'yogesh.pawar@scstechindia.com'],
    'Dhankawadi-Sahakarnagar': ['dhankawadi@punecorporation.org','dhankawadi@punecorporation.org',
                                'vikramkathawate1270@gmail.com', 'vinayak.kadam@scstechindia.com',
                                'nilesh.jadhav@scstechindia.com', 'rutik.pisal@scstechindia.com', 'hariprasad.dandime@scstechindia.com', 'ajay.kedar@scstechindia.com', 'yogesh.pawar@scstechindia.com'],
    'Dhole Patil Road': ['dholepatil@punecorporation.org', 'nikhilshendge741@gmail.com', 'suniltanwar8352@gmail.com',
                         'nanaso.kodag@scstechindia.com', 'ajit.patil@scstechindia.com', 'sujit.sarwade@scstechindia.com', 'hariprasad.dandime@scstechindia.com', 'ajay.kedar@scstechindia.com', 'yogesh.pawar@scstechindia.com'],
    'Hadapsar-Mundhawa': ['Hadapsar@punecorporation.org','Hadapsar@punecorporation.org','naikshripad29@gmil.com',
                          'hemraj.ghane@scstechindia.com', 'prashant.bhosale@scstechindia.com',
                          'vaibhav.savant@scstechindia.com', 'hariprasad.dandime@scstechindia.com', 'ajay.kedar@scstechindia.com', 'yogesh.pawar@scstechindia.com'],
    'Kasba-Vishrambagwada': ['ksaba_vishrambaugwada@punecorporation.org', 'vishu10107@gmail.com',
                             'nmahangre22@gmail.com', 'prathmesh.waghmare@scstechindia.com',
                             'atik.m.sayyed@gmail.com', 'amitghag141077@gmail.com', 'lvkothere@gmail.com',
                             'prathmesh.bhambure@scstechindia.com', 'rakesh.kshirsagar@scstechindia.com',
                             'hariprasad.dandime@scstechindia.com', 'ajay.kedar@scstechindia.com', 'yogesh.pawar@scstechindia.com'],
    'Kondhwa-Yewalewadi': ['kondhwa@punecorporation.org', 'kadamjalu913@gmail.com', 'rohit.bhiwgade@scstechindia.com',
                           'govind.shegar@scstechindia.com', 'nikhil.patil@scstechindia.com', 'hariprasad.dandime@scstechindia.com', 'ajay.kedar@scstechindia.com', 'yogesh.pawar@scstechindia.com'],
    'Kothrud-Bawdhan': ['wmo07.kothrudpmc@gmail.com', 'sachinlohakare99@gmail.com', 'kothrud@punecorporation.org',
                        'rohit.suryawanshi@scstechindia.com', 'eknath.mali@scstechindia.com',
                        'siddhant.sohani@scstechindia.com', 'hariprasad.dandime@scstechindia.com', 'ajay.kedar@scstechindia.com', 'yogesh.pawar@scstechindia.com'],
    'Nagar Road - Wadgaon Sheri': ['nagarroad@punecorporation.org', 'sandesh1678@gmail.com',
                                   'shailesh.badadal@scstechindia.com', 'vivek.ayawale@scstechindia.com',
                                   'dattaraj.patil@scstechindia.com', 'hariprasad.dandime@scstechindia.com', 'ajay.kedar@scstechindia.com', 'yogesh.pawar@scstechindia.com'],
    'Shivajinagar-Ghole Road': ['gholerd.healthdep1@gmail.com','Gwo@punecorporation.org','nilimaskakade1973@gmail.com',
                                'umesh.patil@scstechindia.com', 'vinod.patil@scstechindia.com',
                                'navanath.s@scstechindia.com', 'hariprasad.dandime@scstechindia.com', 'ajay.kedar@scstechindia.com', 'yogesh.pawar@scstechindia.com'],
    'Sinhgad Road': ['healthsinhgadroad@gmail.com','sandip.khalate@punecorporation.org','ketannikam@gmail.com',
                     'chandrakantlad@gmail.com', 'sujit.kale@scstechindia.com', 'rupesh.bengade@scstechindia.com',
                     'ulhas.kharde@scstechindia.com', 'hariprasad.dandime@scstechindia.com', 'ajay.kedar@scstechindia.com', 'yogesh.pawar@scstechindia.com'],
    'Wanawadi-Ramtekdi': ['wanawadi@punecorporation.org','nisar.rashid.@gmail.com',
                          'pranit.patil@scstechindia.com', 'abhishek.nikam@scstechindia.com',
                          'pratik.purandare@scstechindia.com', 'hariprasad.dandime@scstechindia.com', 'ajay.kedar@scstechindia.com', 'yogesh.pawar@scstechindia.com'],
    'Warje-Karvenagar': ['warjekarvenagar@punecorporation.org','warjekarvenagar@punecorporation.org',
                         'ganesh.khirid9@gmail.com', 'avinash.faltankar@scstechindia.com',
                         'sanket.jadhav@scstechindia.com', 'avinash.gavhane@scstechindia.com', 'hariprasad.dandime@scstechindia.com', 'ajay.kedar@scstechindia.com', 'yogesh.pawar@scstechindia.com'],
    'Yerawada - Kalas - Dhanori': ['yerwada@punecorporation.org', 'mayurmandhare89@Gmail.com',
                                   'swapnilkutal96@gmail.com', 'pavankumar.patil@scstechindia.com',
                                   'sachin.gaikwad@scstechindia.com', 'lakhan.tekale@scstechindia.com',
                                   'hariprasad.dandime@scstechindia.com', 'ajay.kedar@scstechindia.com', 'yogesh.pawar@scstechindia.com']
}

smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_user = 'info@scstechindia.com'
smtp_password = 'Super123$%'
from_email = 'info@scstechindia.com'

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

# Function to send email
def send_email(subject, body, to_email, filename):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ", ".join(to_email)
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))

    # Attach the Excel file
    with open(filename, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(part)

    # Connect to SMTP server and send email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(from_email, to_email, msg.as_string())


# Loop through each group and send email
for ward, group in wardwise_groups:
    subject = f"CTPT Report Email from SCS for {ward}"

    # Get top 10 rows as HTML table
    top_10_rows_html = group.head(10)
    dataframe_html = dataframe_to_html(top_10_rows_html)

    # Save the full group data to an Excel file
    filename = f"{ward}_report.xlsx"
    group[selected_columns].to_excel(filename, index=False)

    # Full body of the email
    body = f"""
    <html>
    <body>
    <p>Dear Recipient,</p>
    <p>Please find snippet of CTPT details from {ward} and a detailed spreadsheet of invalid and unvisited CTPT in the attachment:</p>
    {dataframe_html}
    <p>Best regards,<br>SCS Team</p>
    <p style="color: gray; font-size: 12px;">This is an auto-generated email, please do not reply.</p>
    </body>
    </html>
    """
    to_email_2 = ward_email_map.get(ward, '')  # Get the email address from ward_emails

    if to_email_2:
        print(f"Sending email for ward: {ward} to {to_email_2}")
        send_email(subject, body, to_email_2, filename)
    else:
        print(f"No email address found for {ward}. Skipping...")

print("All report emails have been sent successfully.")

connection.close()