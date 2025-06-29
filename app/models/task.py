import uuid
from datetime import datetime, timedelta

class Task:
    def __init__(self, title, owner, days, start=None, end=None, id=None):
        self.id = id or str(uuid.uuid4())
        self.title = title
        self.owner = owner
        self.days = int(days)  # duración original fija

        # Start puede venir None, en ese caso usamos hoy
        self.start = start or datetime.today()

        # Solo calculamos end si NO viene dado
        if end is not None:
            self.end = end
        else:
            # Calculamos end solo si no se pasó explícitamente
            self.end = self.start + timedelta(days=self.days - 1)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "owner": self.owner,
            "start": self.start.strftime("%Y-%m-%d"),
            "end": self.end.strftime("%Y-%m-%d"),
            "days": self.days,  # recomendación: guardá days también en el CSV
        }