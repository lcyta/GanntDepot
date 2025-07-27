from app.models.task import Task
import pandas as pd
from typing import List

def from_dataframe(df: pd.DataFrame) -> List[Task]:
    tasks = []
    for _, row in df.iterrows():
        task = Task(
            id=row.get("id"),
            title=row.get("title"),
            owner=row.get("owner"),
            start=(
                pd.to_datetime(row["start"]) 
                if pd.notna(row.get("start")) 
                else None
            ),
            end=(
                pd.to_datetime(row["end"]) 
                if pd.notna(row.get("end")) 
                else None
            ),
            days=int(row.get("days", 1)),
            estado=row.get("estado"),
            riesgo=row.get("riesgo"),
            tipo=row.get("tipo")
        )
        tasks.append(task)
    return tasks


def to_dataframe(tasks: List[Task]) -> pd.DataFrame:
    return pd.DataFrame([t.to_dict() for t in tasks])
