from app.core.firestore import db
from app.modules.match.models.match import Match


class FindEventCommand:
    def __init__(self, match):
        self.match = match

    def execute(self):
        return db.collection(Match.COLLECTION).document(str(self.match.id)).get().to_dict()
