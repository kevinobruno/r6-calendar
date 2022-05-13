import json

from app.core.google_calendar import GoogleCalendar


class UpdateEventCommand:
    def __init__(self, match, event_id):
        self.match = match
        self.event_id = event_id

    def execute(self):
        GoogleCalendar().update_event(match=self.match, event_id=self.event_id)

        file = open('matches_scheduled.json')
        matches_scheduled = json.load(file)

        matches_scheduled[self.match.id] = {
            'event_id': self.event_id,
            'match': self.match.dict(),
        }

        file = open('matches_scheduled.json', 'w')
        json.dump(matches_scheduled, file)
