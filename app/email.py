import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os


def send_reset_password_email(recipient_email: str, reset_url: str):
    # setting for send email
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = os.getenv("SMTP_USER_NAME")
    smtp_password = os.getenv("SMTP_PASSWORD")

    # Create text letter
    subject = "Password reset"
    body = f"To reset your password, follow the following link: {reset_url}"

    # Create odj. letter
    msg = MIMEMultipart()
    msg["From"] = smtp_username
    msg["To"] = recipient_email
    msg["Subject"] = subject

    # Add text letter
    msg.attach(MIMEText(body, "plain"))

    # Connect to the SMTP server and send a letter
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, recipient_email, msg.as_string())
        server.quit()

    except Exception as e:
        # Handling errors when sending
        print(f"Error send message: {str(e)}")
