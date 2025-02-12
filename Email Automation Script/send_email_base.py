import smtplib

sender_email = input("Sender Email Address: ")
receiver_email = input("Receiver Email Address: ")

subject = input("Subject: ")
message = input("Message: ")

text = f"Subject: {subject}\n\n{message}"

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()

server.login(sender_email, "mjly jzhz vadw lwrd")

server.sendmail(sender_email, receiver_email, text)

print("Email has been sent to "+receiver_email)