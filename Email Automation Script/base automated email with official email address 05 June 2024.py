import smtplib

# Email details
sender_email = "info@scstechindia.com"
sender_password = "Super123$%"
receiver_email = "sweta.rai@scstechindia.com"

subject = f"Automated Report Email from SCS"
message = f"""
    <html>
    <body>
    <p>Dear Recipient,</p>
    <p>Testing out the new official email address here.</p>
    <p>Best regards,<br>SCS Team</p>
    <p style="color: gray; font-size: 12px;">This is an auto-generated email, please do not reply.</p>
    </body>
    </html>
    """

text = f"Subject: {subject}\n\n{message}"

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()

server.login(sender_email, sender_password)

server.sendmail(sender_email, receiver_email, text)

print("Email has been sent to "+receiver_email)