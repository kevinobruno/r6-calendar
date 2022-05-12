import json
import os

from google.oauth2 import service_account
from googleapiclient.discovery import build


class GoogleCalendar:

    CALENDARS = {
        'ASIA': '',
        'BR': 'e2njd3v1ib1m7vu1cehrhh9rb4@group.calendar.google.com',
        'LATAM': '',
        'EU': '',
        'GLOBAL': 'oemr33rodalfi44e04mrtamnac@group.calendar.google.com',
    }

    DEFAULT_TIMEZONE = 'America/Sao_Paulo'
    DEAFULT_TZ_INFO = '-03:00'

    def __init__(self):
        credentials_info = json.load(os.environ['GOOGLE_CREDENTIALS'])
        credentials = service_account.Credentials.from_service_account_info(credentials_info)
        self.service = build('calendar', 'v3', credentials=credentials)

    def create_event(self, match):
        calendar_id = self.CALENDARS[match.championship.region]

        event = {
            'summary': match.summary,
            'description': None,
            'start': {
                'dateTime': f'{match.start.strftime("%Y-%m-%dT%H:%M:%S")}{self.DEAFULT_TZ_INFO}',
                'timeZone': self.DEFAULT_TIMEZONE,
            },
            'end': {
                'dateTime': f'{match.end.strftime("%Y-%m-%dT%H:%M:%S")}{self.DEAFULT_TZ_INFO}',
                'timeZone': self.DEFAULT_TIMEZONE,
            },
        }

        return self.service.events().insert(calendarId=calendar_id, body=event).execute()
