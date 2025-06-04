import datetime
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from birthday_reminder import calculate_days_until

def test_calculate_days_until_future():
    today = datetime.date(2024, 6, 1)
    birthday = datetime.date(1990, 6, 15)
    assert calculate_days_until(birthday, today) == 14


def test_calculate_days_until_next_year():
    today = datetime.date(2024, 6, 16)
    birthday = datetime.date(1990, 6, 15)
    # Next occurrence will be next year
    assert calculate_days_until(birthday, today) == 364
