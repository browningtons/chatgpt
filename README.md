# Birthday Reminder Tool

This repository contains a Python script (`birthday_reminder.py`) that checks a Google Sheet for upcoming birthdays and sends reminders via Twilio and email.

- Reads a Google Sheet of names, birthdays, and phone numbers.
- Sends SMS reminders 14 and 7 days before a birthday.
- Sends an automatic "Happy Birthday" email at 7:30 AM on the birthday.
## Setup

1. **Install Dependencies**

   SMTP_SERVER=smtp.example.com
   SMTP_PORT=587
   SMTP_USERNAME=user@example.com
   SMTP_PASSWORD=your_password
   EMAIL_FROM=user@example.com
   Set `MOCK_MODE=true` to print SMS content instead of sending via Twilio. The repository includes a `.gitignore` so that your `.env` file won't be committed by accident.
   - Share your Google Sheet with the service account email.

4. **Running the Script**
   - Run once immediately:
     ```bash
     python birthday_reminder.py --now
     ```
   - Or start the scheduler which checks daily at 7 AM:
     ```bash
     python birthday_reminder.py
     ```
5. **Tests**
   ```bash
   pytest -q
   ```
## Notes

- Network access may be required for Google Sheets, Twilio, and your SMTP server.
