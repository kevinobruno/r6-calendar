import datetime
import json


class BaseModel:
    def dict(self):
        def json_default(value):
            if isinstance(value, datetime.date):
                return value.isoformat()
            return value.__dict__

        return json.loads(json.dumps(self, default=json_default))
