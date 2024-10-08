import smtplib
import logging
from email.mime.text import MIMEText
from config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER

def send_email_notification(release_id, release_title, new_sellers):
    subject = f"New sellers for Release {release_id} - {release_title}" 
    sellers_list = "\n".join(new_sellers)
    body = f"""New sellers detected for release {release_id}:
{sellers_list}

You can view the release here: https://www.discogs.com/sell/release/{release_id}
"""
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, [EMAIL_RECEIVER], msg.as_string())
        logging.info(f"Notification sent for release {release_id} - {release_title}")