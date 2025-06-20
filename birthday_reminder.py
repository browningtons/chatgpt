import os
import datetime
import logging
import argparse
from typing import List

from dotenv import load_dotenv

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
import json

# Load environment variables from .env if available
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Static list of gift ideas used if network access is unavailable.
STATIC_GIFT_IDEAS = [
    "Gift idea 1 - https://example.com/product1",
    "Gift idea 2 - https://example.com/product2",
    "Gift idea 3 - https://example.com/product3",
    "Gift idea 4 - https://example.com/product4",
    "Gift idea 5 - https://example.com/product5",
]

MOCK_MODE = os.getenv("MOCK_MODE", "false").lower() == "true"
CUSTOM_MESSAGES_FILE = os.getenv("CUSTOM_MESSAGES_FILE", "custom_messages.json")

def fetch_gift_ideas(person_name: str) -> List[str]:
    """Return a list of gift idea strings."""
    # In a real setup, this might query an online store's API.
    # Here we return a static list due to environment limits.
    return STATIC_GIFT_IDEAS


def calculate_days_until(birthday: datetime.date, today: datetime.date | None = None) -> int:
    """Return days until the next occurrence of birthday."""
    if today is None:
        today = datetime.date.today()
    upcoming = birthday.replace(year=today.year)
    if upcoming < today:
        upcoming = upcoming.replace(year=today.year + 1)
    return (upcoming - today).days


def get_sheet_records() -> List[dict]:
    """Fetch records from the Google Sheet."""
    sheet_id = os.environ.get("SHEET_ID")
    worksheet_name = os.environ.get("WORKSHEET", "Birthdays")
    creds_path = os.environ.get("GOOGLE_CREDS_JSON")
    if not sheet_id or not creds_path:
        raise RuntimeError("SHEET_ID and GOOGLE_CREDS_JSON must be set")
    if gspread is None or ServiceAccountCredentials is None:
        raise RuntimeError("gspread is required to access Google Sheets")

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.worksheet(worksheet_name)
    return worksheet.get_all_records()


def send_sms(to: str, body: str):
    """Send an SMS message using Twilio or log in mock mode."""
    if MOCK_MODE:
        logger.info("[MOCK] SMS to %s: %s", to, body)
        return
    if Client is None:
        raise RuntimeError("twilio is required to send SMS")
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    from_phone = os.environ.get("TWILIO_FROM_PHONE")
    if not account_sid or not auth_token or not from_phone:
        raise RuntimeError("Twilio credentials are not fully configured")

    client = Client(account_sid, auth_token)
    client.messages.create(to=to, from_=from_phone, body=body)


def load_custom_messages() -> dict:
    """Load custom messages from disk."""
    if os.path.exists(CUSTOM_MESSAGES_FILE):
        try:
            with open(CUSTOM_MESSAGES_FILE, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except Exception as exc:
            logger.error("Failed to read %s: %s", CUSTOM_MESSAGES_FILE, exc)
    return {}


def save_custom_messages(messages: dict) -> None:
    """Persist custom messages to disk."""
    try:
        with open(CUSTOM_MESSAGES_FILE, "w", encoding="utf-8") as fh:
            json.dump(messages, fh)
    except Exception as exc:
        logger.error("Failed to write %s: %s", CUSTOM_MESSAGES_FILE, exc)


def check_birthdays(prompt: bool = False):
    """Check the sheet for upcoming birthdays and send reminders."""
    try:
        records = get_sheet_records()
    except Exception as exc:
        logger.error("Error fetching sheet records: %s", exc)
        return

    now = datetime.datetime.now()
    user_phone = os.environ.get("USER_PHONE")
    messages = load_custom_messages()
    for rec in records:
        name = rec.get("name") or rec.get("Name")
        birthday_str = rec.get("birthday") or rec.get("Birthday")
        phone = rec.get("phone") or rec.get("Phone")
        if not name or not birthday_str:
            continue
        try:
            bday = datetime.datetime.strptime(birthday_str, "%Y-%m-%d")
        except ValueError:
            logger.error("Invalid date format for %s: %s", name, birthday_str)
            continue

        days_until = calculate_days_until(bday.date(), now.date())
        upcoming = bday.replace(year=now.year)
        if upcoming < now:
            upcoming = upcoming.replace(year=now.year + 1)

        key = f"{name}|{upcoming:%Y-%m-%d}"

        if days_until == 14 and user_phone:
            ideas = fetch_gift_ideas(name)
            body = f"Reminder: {name}'s birthday is on {upcoming:%Y-%m-%d}.\n" + "\n".join(ideas)
            try:
                send_sms(user_phone, body)
            except Exception as exc:
                logger.error("Error sending SMS reminder: %s", exc)
            if prompt and key not in messages:
                user_msg = input(
                    f"Enter birthday message for {name} to send on {upcoming:%Y-%m-%d} (blank to skip): "
                ).strip()
                if user_msg:
                    messages[key] = user_msg
                    save_custom_messages(messages)

        if days_until == 0 and phone:
            custom = messages.pop(key, None)
            if custom is not None:
                message = custom
                save_custom_messages(messages)
            else:
                message = f"Happy Birthday, {name}!"
            run_time = datetime.datetime.combine(upcoming.date(), datetime.time(7, 30))
            scheduler.add_job(send_sms, "date", run_date=run_time, args=[phone, message])
            logger.info("Scheduled birthday message for %s at %s", name, run_time)


scheduler = BlockingScheduler()
# Run check_birthdays every day at 7am
scheduler.add_job(check_birthdays, "cron", hour=7, minute=0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Birthday reminder")
    parser.add_argument("--now", action="store_true", help="Run birthday check immediately and exit")
    parser.add_argument("--prompt", action="store_true", help="Prompt for custom birthday messages")
    args = parser.parse_args()

    if args.now:
        check_birthdays(prompt=args.prompt)
    else:
        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            pass
