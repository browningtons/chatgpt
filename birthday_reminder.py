import os
import datetime

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

# Static list of gift ideas used if network access is unavailable.
STATIC_GIFT_IDEAS = [
    "Gift idea 1 - https://example.com/product1",
    "Gift idea 2 - https://example.com/product2",
    "Gift idea 3 - https://example.com/product3",
    "Gift idea 4 - https://example.com/product4",
    "Gift idea 5 - https://example.com/product5",
]

def fetch_gift_ideas(person_name: str) -> List[str]:
    """Return a list of gift idea strings."""
    # In a real setup, this might query an online store's API.
    # Here we return a static list due to environment limits.
    return STATIC_GIFT_IDEAS

    client = Client(account_sid, auth_token)
    client.messages.create(to=to, from_=from_phone, body=body)

    """Check the sheet for upcoming birthdays and send reminders."""
    try:
        records = get_sheet_records()
    except Exception as exc:
        return

    now = datetime.datetime.now()
    user_phone = os.environ.get("USER_PHONE")

    for rec in records:
        name = rec.get("name") or rec.get("Name")
        birthday_str = rec.get("birthday") or rec.get("Birthday")
        phone = rec.get("phone") or rec.get("Phone")
        if not name or not birthday_str:
            continue
        try:
            bday = datetime.datetime.strptime(birthday_str, "%Y-%m-%d")
        except ValueError:

        if days_until == 14 and user_phone:
            ideas = fetch_gift_ideas(name)
            body = f"Reminder: {name}'s birthday is on {upcoming:%Y-%m-%d}.\n" + "\n".join(ideas)
            try:
                send_sms(user_phone, body)

scheduler = BlockingScheduler()
# Run check_birthdays every day at 7am
scheduler.add_job(check_birthdays, "cron", hour=7, minute=0)

if __name__ == "__main__":
