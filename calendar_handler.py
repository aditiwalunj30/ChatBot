from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import datetime
import json

# Scopes = what permissions you’re requesting
SCOPES = ['https://www.googleapis.com/auth/calendar']

# ✅ Test if credentials file exists and is valid
def test_credentials_file():
    try:
        with open("../credentials/credentials.json", "r") as f:
            data = f.read()
            print("✅ credentials.json file is readable.")
            print("First 100 characters:\n", data[:100])
            json.loads(data)  # Check if it's valid JSON
            print("✅ JSON format is valid.")
    except FileNotFoundError:
        print("❌ File not found. Check the path.")
    except json.JSONDecodeError:
        print("❌ File is not valid JSON.")
    except Exception as e:
        print("❌ Other error:", e)

# ✅ Authenticate with Google Calendar
def get_calendar_service():
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials/credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    service = build('calendar', 'v3', credentials=creds)
    return service

# ✅ List upcoming 5 events
def list_upcoming_events():
    service = get_calendar_service()
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' = UTC time
    print('Getting the upcoming 5 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=5, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
        return []

    output = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        output.append(f"{start} - {event.get('summary', 'No Title')}")
    return output

# ✅ Book a new event
def book_event(summary, start_time_str, end_time_str):
    service = get_calendar_service()

    event = {
        'summary': summary,
        'start': {
            'dateTime': start_time_str,
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_time_str,
            'timeZone': 'Asia/Kolkata',
        },
    }

    event_result = service.events().insert(calendarId='primary', body=event).execute()
    return f"✅ Event created: {event_result.get('htmlLink')}"

# ✅ Run as test script
if __name__ == "__main__":
    test_credentials_file()  # Optional: checks if the credentials file is valid

    print("\nUpcoming events:")
    events = list_upcoming_events()
    for e in events:
        print(e)

    print("\nBooking a test meeting...")
    summary = "Test Meeting with TailorTalk"
    start_time = "2025-06-26T15:00:00"
    end_time = "2025-06-26T15:30:00"
    result = book_event(summary, start_time, end_time)
    print(result)
