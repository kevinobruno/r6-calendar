import json


class FindEventCommand:
    def __init__(self, match):
        self.match = match
        self.matches_scheduled = None

    def execute(self):
        with open('matches_scheduled.json') as file:
            self.matches_scheduled = json.load(file)

        return self.matches_scheduled.get(str(self.match.id), False)
