import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from birthday_reminder import fetch_gift_ideas

def test_gift_ideas_count():
    ideas = fetch_gift_ideas('Alice')
    assert isinstance(ideas, list)
    assert len(ideas) >= 5
