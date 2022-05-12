from datetime import datetime
import json

from bs4 import BeautifulSoup
import requests

from app.modules.match.models.championship import Championship
from app.modules.match.models.match import Match
from app.modules.match.models.team import Team


class BaseListMatchesCommand:

    CHAMPIONSHIP_ID_LIST = {
        'ASIA': [
            24,  # Asia-Pacific League - Playoffs
        ],
        'BR': [
            9,   # Circuito Feminino de Rainbow Six
            11,  # Copa do Brasil
        ],
        'LATAM': [
            3,   # Copa da América do Sul
            8,   # Copa Elite Six da América
        ],
        'EU': [
            19,  # Liga Européia
        ],
        'GLOBAL': [
            25,  # Six Major Charlotte
        ],
    }

    CHAMPIONSHIP_REGION = ''

    def execute(self):
        response = requests.get('https://www.r6esportsbr.com/pt/calendar/')
        html = response.text
        soup = BeautifulSoup(html)

        data = json.loads(soup.find(id='__NEXT_DATA__').text)

        results = data['props']['pageProps']['matches']
        matches = []

        for r in results:
            championship = Championship(
                id=r['championship']['id'],
                name=r['championship']['name'],
                region=self.CHAMPIONSHIP_REGION,
            )

            self._map_championship(championship)

            # Ignore matches in the past
            timestamp = int(r['date']['timestamp'])
            if timestamp < datetime.now().timestamp():
                continue

            # Ignore not wanted championship
            if championship.id not in self.CHAMPIONSHIP_ID_LIST[self.CHAMPIONSHIP_REGION]:
                continue

            team1 = Team(id=r['team1']['id'], name=r['team1']['name'], score=r['team1']['score'])
            team2 = Team(id=r['team2']['id'], name=r['team2']['name'], score=r['team2']['score'])

            # Ignore matches that doesn't have both teams determined
            if team1.name == 'None' or team2.name == 'None':
                continue

            match = Match(
                id=r['id'],
                championship=championship,
                team1=team1,
                team2=team2,
                timestamp=r['date']['timestamp'],
                start=r['date']['datetime'],
            )

            matches.append(match)

        return matches

    def _map_championship(self, championship):
        file = open('mapped_championships.json')
        mapped_championships = json.load(file)

        if not mapped_championships.get(str(championship.id)):
            file = open('mapped_championships.json', 'w')
            mapped_championships[championship.id] = championship.name
            json.dump(mapped_championships, file)

            # TODO: Notify somewhere else like email
            print(f'New championship mapped {championship.id} - {championship.name}')
