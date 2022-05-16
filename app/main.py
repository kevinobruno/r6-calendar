from app.modules.event.commands.create import CreateEventCommand
from app.modules.event.commands.flush import FlushEventsCommand
from app.modules.event.commands.find import FindEventCommand
from app.modules.event.commands.update import UpdateEventCommand
from app.modules.match.commands.list.br import ListBRMatches
from app.modules.match.commands.list.mundial import ListMundialMatches


matches = []

matches.extend(ListBRMatches().execute())
matches.extend(ListMundialMatches().execute())

print(f'{len(matches)} matches found')

# print('Flushing events...')
# FlushEventsCommand(championship_id=25).execute()

for match in matches:
    event = FindEventCommand(match=match).execute()

    if event:
        print(f'Match {match.summary} event already created, updating if needed...')
        UpdateEventCommand(match=match, event_id=event['event_id']).execute()
        continue

    print(f'Creating event for match {match.summary} ...')
    CreateEventCommand(match=match).execute()
