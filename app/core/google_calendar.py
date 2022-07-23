import json
import os

from app.core.parameter_store import ParameterStore

from google.oauth2 import service_account
from googleapiclient.discovery import build


class GoogleCalendar:

    CALENDARS = {
        'ASIA': os.environ['ASIA_CALENDAR_ID'],
        'BR': os.environ['BR_CALENDAR_ID'],
        'EU': os.environ['EU_CALENDAR_ID'],
        'GLOBAL': os.environ['GLOBAL_CALENDAR_ID'],
        'LATAM': os.environ['LATAM_CALENDAR_ID'],
        'NA': os.environ['NA_CALENDAR_ID'],
    }

    DEFAULT_TIMEZONE = 'America/Sao_Paulo'
    DEAFULT_TZ_INFO = '-03:00'

    def __init__(self):
        parameter_store = ParameterStore()
        credentials_info = json.loads(parameter_store.get(name='GOOGLE_CREDENTIALS'))
        credentials = service_account.Credentials.from_service_account_info(credentials_info)
        self.service = build('calendar', 'v3', credentials=credentials)

    def create_event(self, match):
        calendar_id = self.CALENDARS[match.championship.region]

        event = {
            'summary': match.summary,
            'description': match.championship.name,
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

    def update_event(self, match, event_id):
        calendar_id = self.CALENDARS[match.championship.region]

        event = self.service.events().get(calendarId=calendar_id, eventId=event_id).execute()

        event['summary'] = match.summary
        event['description'] = match.championship.name
        event['start']['dateTime'] = f'{match.start.strftime("%Y-%m-%dT%H:%M:%S")}{self.DEAFULT_TZ_INFO}'
        event['end']['dateTime'] = f'{match.end.strftime("%Y-%m-%dT%H:%M:%S")}{self.DEAFULT_TZ_INFO}'

        self.service.events().update(
            calendarId=calendar_id,
            eventId=event['id'],
            body=event,
        ).execute()

    def delete_event(self, championship_region, event_id):
        calendar_id = self.CALENDARS[championship_region]
        self.service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
