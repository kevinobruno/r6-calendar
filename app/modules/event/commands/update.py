from app.core.firestore import db
from app.core.google_calendar import GoogleCalendar
from app.modules.event.commands.find import FindEventCommand
from app.modules.match.models.match import Match


class UpdateEventCommand:
    def __init__(self, match, event_id):
        self.match = match
        self.event_id = event_id

    def execute(self):
        event = FindEventCommand(match=self.match).execute()

        if event['match']['summary'] == self.match.summary:
            return

        GoogleCalendar().update_event(match=self.match, event_id=self.event_id)

        data = {'google_calendar_event_id': self.event_id, 'match': self.match.dict()}
        db.collection(Match.COLLECTION).document(str(self.match.id)).set(data)
