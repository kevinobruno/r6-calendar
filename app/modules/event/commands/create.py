import json

from app.core.google_calendar import GoogleCalendar


class CreateEventCommand:
    def __init__(self, match):
        self.match = match
        self.matches_scheduled = None

    def execute(self):
        event = GoogleCalendar().create_event(match=self.match)

        with open('matches_scheduled.json') as file:
            self.matches_scheduled = json.load(file)

        self.matches_scheduled[self.match.id] = {'event_id': event['id']}

        with open('matches_scheduled.json', 'w') as file:
            json.dump(self.matches_scheduled, file)
