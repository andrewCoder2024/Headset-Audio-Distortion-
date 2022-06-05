import smtplib
import os
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


# cS.ZP_984xk6gJs
def email_excel(sender_email="pythontest680@gmail.com", receiver_email="pythontest680@gmail.com",
                subject="An email with attachment from Python",
                body="This is an email with attachment sent from Python"):
    password = input("Type your password and press enter:")
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))
    body = MIMEText(body, 'html', 'utf-8')
    message.attach(body)  # add message body (text or html)
    dir_path = os.getcwd()
    files = [file for file in os.listdir("/Users/andrewlustig/PycharmProjects/RealWare Sound Recognition")
             if file.endswith('xlsx')]
    for f in files:  # add files to the message
        file_path = os.path.join(dir_path, f)
        attachment = MIMEApplication(open(file_path, "rb").read(), _subtype="txt")
        attachment.add_header('Test Files', 'attachment', filename=f)
        message.attach(attachment)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())


email_excel()
