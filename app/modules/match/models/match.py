from datetime import date
from datetime import datetime, timedelta

from app.core.model import BaseModel


class Match(BaseModel):

    DEFAULT_MATCH_DURATION = 60  # minutes
    DEFAULT_TZ_INFO = '-0300'

    def __init__(self, id, timestamp, start, championship, team1, team2):
        self.id = int(id)
        self.timestamp = timestamp
        self.championship = championship
        self.team1 = team1
        self.team2 = team2

        date, time = start.split(' ')
        self.start = datetime.strptime(f'{date}T{time}{self.DEFAULT_TZ_INFO}', '%Y-%m-%dT%H:%M:%S%z')
        self.end = self.start + timedelta(minutes=self.DEFAULT_MATCH_DURATION)

        self.summary = f'{self.team1.name} vs {self.team2.name}'

        if self.team1.score != 0 or self.team2.score != 0:
            self.summary = f'{self.team1.name} ({self.team1.score}) vs ({self.team2.score}) {self.team2.name}'

    def __str__(self):
        return f'{self.championship.name} | {self.start} | {self.team1.name} vs {self.team2.name}'
