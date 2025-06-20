# Birthday Reminder Tool

## Features

- Reads a Google Sheet of names, birthdays, and phone numbers.
- Sends a reminder 14 days before a birthday with a short list of gift ideas.
- Automatically schedules a "Happy Birthday" message to be sent at 7:30 AM on the birthday.

## Setup

1. **Install Dependencies**

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
