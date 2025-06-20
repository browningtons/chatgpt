import os
import datetime
import smtplib
from email.message import EmailMessage

try:
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
except ImportError:
    gspread = None  # placeholder if not installed
    ServiceAccountCredentials = None

try:
    from twilio.rest import Client
except ImportError:
    Client = None

from apscheduler.schedulers.blocking import BlockingScheduler
    client.messages.create(to=to, from_=from_phone, body=body)

def send_email(to: str, subject: str, body: str):
    """Send an email using SMTP."""
    smtp_server = os.environ.get("SMTP_SERVER")
    smtp_port = int(os.environ.get("SMTP_PORT", 587))
    smtp_user = os.environ.get("SMTP_USERNAME")
    smtp_pass = os.environ.get("SMTP_PASSWORD")
    from_addr = os.environ.get("EMAIL_FROM")
    if not all([smtp_server, smtp_user, smtp_pass, from_addr]):
        logger.error("SMTP credentials are not fully configured")
        return
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to
    msg.set_content(body)
        with smtplib.SMTP(smtp_server, smtp_port) as smtp:
            smtp.starttls()
            smtp.login(smtp_user, smtp_pass)
            smtp.send_message(msg)
        logger.error("Error sending email: %s", exc)
def check_birthdays():
            bday = datetime.datetime.strptime(birthday_str, "%Y-%m-%d")
        except ValueError:

        if days_until in (14, 7) and user_phone:
            body = f"Reminder: {name}'s birthday is on {upcoming:%Y-%m-%d}."

        if days_until == 0 and rec.get("email"):
            subject = f"Happy Birthday, {name}!"
            body = f"Wishing you a wonderful birthday, {name}!"
            scheduler.add_job(send_email, "date", run_date=run_time, args=[rec.get("email"), subject, body])
            logger.info("Scheduled birthday email for %s at %s", name, run_time)
        check_birthdays()
