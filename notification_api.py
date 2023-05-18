import smtplib, ssl
from email.message import EmailMessage

def send_email():
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "davidcomputer114@gmail.com"  
    receiver_email = "davidcomputer114@gmail.com"  
    password = "avzuyrwosewmelkl"

    msg = EmailMessage()
    msg.set_content("The weather has changed for an event that you are planning.\n"
                    "Please check the app and plan accordingly.\n")
    msg['Subject'] = "Weather has changed for an event"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.send_message(msg, from_addr=sender_email, to_addrs=receiver_email)

    return
