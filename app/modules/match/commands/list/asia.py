from lib2to3.pytree import Base
from app.modules.match.commands.list.base import BaseListMatchesCommand


class ListAsiaMatches(BaseListMatchesCommand):

    CHAMPIONSHIP_REGION = 'ASIA'
