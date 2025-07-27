import uuid
from datetime import datetime, timedelta

class Task:
    def __init__(self, title, owner, days, start=None, end=None, id=None, riesgo=None, tipo=None, estado=None):
        self.id = id or str(uuid.uuid4())
        self.title = title
        self.owner = owner
        self.days = int(days)

        self.riesgo = riesgo
        self.tipo = tipo
        self.estado = estado

        self.start = start or datetime.today()

        if end is not None:
            self.end = end
        else:
            self.end = self.start + timedelta(days=self.days - 1)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "owner": self.owner,
            "start": self.start.strftime("%Y-%m-%d"),
            "end": self.end.strftime("%Y-%m-%d"),
            "days": self.days,
            "estado": self.estado,
            "riesgo": self.riesgo,
            "tipo": self.tipo,
        }