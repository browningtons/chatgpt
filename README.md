# Birthday Reminder Tool

This repository contains a Python script (`birthday_reminder.py`) that checks a Google Sheet for upcoming birthdays and sends SMS notifications via Twilio.

## Features

- Reads a Google Sheet of names, birthdays, and phone numbers.
- Sends a reminder 14 days before a birthday with a short list of gift ideas.
- Automatically schedules a "Happy Birthday" message to be sent at 7:30 AM on the birthday.
- Supports a mock mode for testing without sending real SMS.
- Optionally prompt for a custom birthday message to send on the big day.

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**
   Copy `.env.example` to `.env` and fill in your credentials. The script uses [python-dotenv](https://github.com/theskumar/python-dotenv) to load these variables automatically.
   The easiest way is:

   ```bash
   cp .env.example .env
   # then edit .env with your favorite editor
   ```

   Replace the placeholder values with your own credentials. A completed `.env` file should look like this:

   ```
   SHEET_ID=your_google_sheet_id
   GOOGLE_CREDS_JSON=/path/to/creds.json
   WORKSHEET=Birthdays
   TWILIO_ACCOUNT_SID=your_twilio_sid
   TWILIO_AUTH_TOKEN=your_twilio_token
   TWILIO_FROM_PHONE=+15555555555
   USER_PHONE=+15555555555
   MOCK_MODE=true
   CUSTOM_MESSAGES_FILE=custom_messages.json
   ```

   You can change `CUSTOM_MESSAGES_FILE` if you want to store custom messages elsewhere. Set `MOCK_MODE=true` to print SMS content instead of sending via Twilio. The repository includes a `.gitignore` so that your `.env` file won't be committed by accident.

3. **Google Sheets Credentials**
   - Create a Google service account and download the credentials JSON file.
   - Share your Google Sheet with the service account email.

4. **Running the Script**
   - Run once immediately (use `--prompt` to provide custom birthday messages):
     ```bash
     python birthday_reminder.py --now --prompt
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
