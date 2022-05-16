import json

from app.core.google_calendar import GoogleCalendar


class FlushEventsCommand:
    def __init__(self, championship_id):
        self.championship_id = championship_id

    def execute(self):
        file = open('matches_scheduled.json') 
        matches_scheduled = json.load(file)

        for match_id, data in list(matches_scheduled.items()):
            match = data['match']
            if self.championship_id == match['championship']['id']:
                GoogleCalendar().delete_event(
                    championship_region=match['championship']['region'],
                    event_id=data['event_id'],
                )

                del matches_scheduled[match_id]

        file = open('matches_scheduled.json', 'w')
        json.dump(matches_scheduled, file)
