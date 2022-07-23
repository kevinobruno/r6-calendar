from app.modules.event.commands.create import CreateEventCommand
from app.modules.event.commands.find import FindEventCommand
from app.modules.event.commands.update import UpdateEventCommand
from app.modules.match.commands.list.asia import ListAsiaMatches
from app.modules.match.commands.list.br import ListBRMatches
from app.modules.match.commands.list.eu import ListEUMatches
from app.modules.match.commands.list.latam import ListLatamMatches
from app.modules.match.commands.list.mundial import ListMundialMatches
from app.modules.match.commands.list.na import ListNAMatches


matches = []

matches.extend(ListAsiaMatches().execute())
matches.extend(ListBRMatches().execute())
matches.extend(ListEUMatches().execute())
matches.extend(ListLatamMatches().execute())
matches.extend(ListMundialMatches().execute())
matches.extend(ListNAMatches().execute())

print(f'{len(matches)} matches found')

for match in matches:
    event = FindEventCommand(match=match).execute()

    if event:
        print(f'Match {match.summary} event already created, updating if needed...')
        UpdateEventCommand(match=match, event_id=event['google_calendar_event_id']).execute()
        continue

    print(f'Creating event for match {match.summary} ...')
    CreateEventCommand(match=match).execute()
