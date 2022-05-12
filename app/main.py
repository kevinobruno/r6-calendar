from app.modules.event.commands.create import CreateEventCommand
from app.modules.event.commands.find import FindEventCommand
from app.modules.match.commands.list.br import ListBRMatches
from app.modules.match.commands.list.mundial import ListMundialMatches


matches = []

matches.extend(ListBRMatches().execute())
matches.extend(ListMundialMatches().execute())

print(f'{len(matches)} matches found')

for match in matches:
    event = FindEventCommand(match=match).execute()

    if event:
        print(f'Match {match.id} event already created, skipping...')
        continue

    print(f'Creating event for match {match.id} ...')
    CreateEventCommand(match=match).execute()
