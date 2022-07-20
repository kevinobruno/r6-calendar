from app.core.firestore import db
from app.core.google_calendar import GoogleCalendar
from app.modules.match.models.match import Match


class CreateEventCommand:
    def __init__(self, match):
        self.match = match

    def execute(self):
        event = GoogleCalendar().create_event(match=self.match)

        data = {'google_calendar_event_id': event['id'], 'match': self.match.dict()}
        db.collection(Match.COLLECTION).document(str(self.match.id)).set(data)
