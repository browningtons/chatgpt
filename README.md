# Birthday Reminder Tool

This repository contains a Python script (`birthday_reminder.py`) that checks a Google Sheet for upcoming birthdays and sends SMS notifications via Twilio.

## Features

- Reads a Google Sheet of names, birthdays, and phone numbers.
- Sends a reminder 14 days before a birthday with a short list of gift ideas.
- Automatically schedules a "Happy Birthday" message to be sent at 7:30 AM on the birthday.
- Supports a mock mode for testing without sending real SMS.

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**
   Copy `.env.example` to `.env` and fill in your credentials. The script uses [python-dotenv](https://github.com/theskumar/python-dotenv) to load these variables automatically.

3. **Google Sheets Credentials**
   - Create a Google service account and download the credentials JSON file.
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

- The gift ideas list is static by default. You can modify the `fetch_gift_ideas` function to integrate with your preferred shopping API.
- Network access may be required for Google Sheets and Twilio APIs.
