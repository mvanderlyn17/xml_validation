import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# AWS Config
EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
EMAIL_HOST_USER = 'foo'
EMAIL_HOST_PASSWORD = 'bar'
EMAIL_PORT = 587

msg = MIMEMultipart('alternative')
msg['Subject'] = "test foo"
msg['From'] = "sender@example.org"
msg['To'] = "receiver@example.org"

html = open('index.html').read()

mime_text = MIMEText(html, 'html')
msg.attach(mime_text)

s = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
s.starttls()
s.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
s.sendmail(me, you, msg.as_string())
s.quit()
