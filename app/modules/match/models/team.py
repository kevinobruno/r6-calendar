from app.core.model import BaseModel


class Team(BaseModel):
    def __init__(self, id, name, score):
        self.id = int(id)
        self.name = str(name)
        self.score = int(score)
