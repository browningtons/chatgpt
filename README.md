# Birthday Reminder Tool

This repository contains a simple Python script (`birthday_reminder.py`) that checks a Google Sheet for upcoming birthdays and sends SMS notifications via Twilio.

## Features

- Reads a Google Sheet of names, birthdays, and phone numbers.
- Sends a reminder 14 days before a birthday with a short list of gift ideas.
- Automatically schedules a "Happy Birthday" message to be sent at 7:30 AM on the birthday.

## Setup

1. **Install Dependencies**
   ```bash
   pip install gspread oauth2client twilio apscheduler
   ```

2. **Google Sheets Credentials**
   - Create a Google service account and download the credentials JSON file.
   - Share your Google Sheet with the service account email.
   - Set the environment variable `GOOGLE_CREDS_JSON` to the path of the credentials file.
   - Set `SHEET_ID` to the ID of your Google Sheet.
   - Optionally set `WORKSHEET` if the sheet tab is not named `Birthdays`.

3. **Twilio Setup**
   - Create a Twilio account and obtain an account SID, auth token, and a Twilio phone number.
   - Set environment variables `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, and `TWILIO_FROM_PHONE`.
   - Set `USER_PHONE` to your personal phone number for reminder messages.

4. **Sheet Format**
   The worksheet should contain columns titled `Name`, `Birthday` (in `YYYY-MM-DD` format), and `Phone`.

5. **Running the Script**
   The script uses `apscheduler` to run daily at 7:00 AM. Launch it with:
   ```bash
   python birthday_reminder.py
   ```

## Notes

- The gift ideas list is static by default. You can modify the `fetch_gift_ideas` function to integrate with your preferred shopping API.
- Network access may be required for Google Sheets and Twilio APIs.
