from lib2to3.pytree import Base
from app.core.model import BaseModel


class Championship(BaseModel):

    COLLECTION = 'championships'

    def __init__(self, id, name, region):
        self.id = int(id)
        self.name = name
        self.region = region
