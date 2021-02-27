import logging
import os
import smtplib, ssl

port = 465
password = os.getenv('MAIL_PASSWORD')
smtp_server = os.getenv('SMTP_SERVER')
sender_email = os.getenv('MAIL_LOGIN')
reveiver_emails = os.getenv('RECEIVER_EMAILS')
reveiver_emails = reveiver_emails.split()
context = ssl.create_default_context()


def send_mail(message):
    subject = 'Server message'
    message = 'Subject: {}\n\n{}'.format(subject, message)
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        for mail in reveiver_emails:
            server.sendmail(sender_email, mail, message)
