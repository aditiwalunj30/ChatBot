import sys
import os

# ✅ ADD THIS FIRST
sys.path.insert(0, r"C:\Users\walun\OneDrive\Desktop\python program\tailor-talk")

# ✅ THEN import from backend
from backend.calendar_handler import book_event

from calendar import timegm
from datetime import datetime, timedelta
import re



# ✅ Very simple intent + datetime extraction
def parse_user_input(message):
    print("🔍 Parsing user input...")
    
    # Example input: "Book a meeting tomorrow at 3 PM"
    message = message.lower()

    if "book" in message and ("meeting" in message or "call" in message):
        # Extract time
        time_match = re.search(r"(\d{1,2})(:\d{2})?\s?(am|pm)", message)
        if time_match:
            hour = int(time_match.group(1))
            meridian = time_match.group(3)

            if meridian == "pm" and hour < 12:
                hour += 12

            # Check for 'tomorrow'
            if "tomorrow" in message:
                date = datetime.now() + timedelta(days=1)
            else:
                date = datetime.now()

            start_time = date.replace(hour=hour, minute=0, second=0, microsecond=0)
            end_time = start_time + timedelta(minutes=30)

            return {
                "intent": "book_meeting",
                "summary": "Meeting booked via TailorTalk",
                "start": start_time.isoformat(),
                "end": end_time.isoformat()
            }

    return {"intent": "unknown", "message": "Sorry, I didn't understand that."}

# ✅ Respond function
def respond(user_input):
    parsed = parse_user_input(user_input)
    if parsed["intent"] == "book_meeting":
        return book_event(parsed["summary"], parsed["start"], parsed["end"])
    else:
        return parsed["message"]
