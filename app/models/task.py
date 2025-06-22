import uuid
from datetime import datetime, timedelta

class Task:
    def __init__(self, title, owner, days, start=None, end=None, id=None):
        self.id = id or str(uuid.uuid4())
        self.title = title
        self.owner = owner
        self.days = int(days)  # Guardamos duración en días
        self.start = start or datetime.today()
        # Calculamos end según start y duración
        self.end = end or (self.start + timedelta(days=self.days - 1))

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "owner": self.owner,
            "start": self.start.strftime("%Y-%m-%d"),
            "end": self.end.strftime("%Y-%m-%d"),
        }