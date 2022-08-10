import json

from bs4 import BeautifulSoup
import requests

from app.core.firestore import db
from app.modules.match.models.championship import Championship
from app.modules.match.models.match import Match
from app.modules.match.models.team import Team


class BaseListMatchesCommand:

    CHAMPIONSHIP_ID_LIST = {
        'ASIA': [
            22,  # Asia-Pacific League - South Division
            23,  # Asia-Pacific League - North Division
            24,  # Asia-Pacific League - Playoffs
        ],
        'BR': [
            1,   # Campeonato Brasileiro
            9,   # Circuito Feminino de Rainbow Six
            11,  # Copa do Brasil
        ],
        'LATAM': [
            3,   # Copa da América do Sul
            5,   # Campeonato Mexicano
            8,   # Copa Elite Six da América
            15,  # Copa do México
            17,  # Campeonato Sulamericano
        ],
        'EU': [
            19,  # Liga Européia
        ],
        'NA': [
            20,  # Liga Americana
        ],
        'GLOBAL': [
            25,  # Six Major Charlotte
            26,  # Six Major Berlin
        ],
    }

    CHAMPIONSHIP_REGION = ''

    def execute(self):
        response = requests.get('https://www.r6esportsbr.com/pt/calendar/')
        html = response.text
        soup = BeautifulSoup(html)

        data = json.loads(soup.find(id='__NEXT_DATA__').text)

        results = data['props']['pageProps']['page']['matches']
        matches = []

        for r in results:
            championship = Championship(
                id=r['championship']['id'],
                name=r['championship']['name'],
                region=self.CHAMPIONSHIP_REGION,
            )

            self._map_championship(championship)

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
        document = db.collection(Championship.COLLECTION).document(str(championship.id)).get()

        if not document.exists:
            data = {'name': championship.name}
            db.collection(Championship.COLLECTION).document(str(championship.id)).set(data)

            # TODO: Notify somewhere else like email
            print(f'New championship mapped {championship.id} - {championship.name}')
