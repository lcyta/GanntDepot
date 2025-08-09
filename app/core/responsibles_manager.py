from app.core.data_access.responsible_repository import ResponsibleRepository
from app.core.calendar.calendar_service import CalendarService
import pandas as pd

_repo = ResponsibleRepository()
_calendar = CalendarService()

def load_responsibles():
    df = _repo.load_all()
    return df.to_dict("records")

def save_responsible(name, location, factory):
    df = _repo.load_all()
    df_new = pd.DataFrame([{"name": name, "location": location, "factory": factory}])
    df_combined = pd.concat([df, df_new], ignore_index=True)
    df_combined.drop_duplicates(subset=["name"], inplace=True)
    _repo.save_all(df_combined)
    _calendar.assign_base_if_needed(name, location)

def delete_responsible_by_name(name):
    df = _repo.load_all()
    df_filtered = df[df["name"] != name]
    _repo.save_all(df_filtered)
    _calendar.remove_calendar_if_exists(name)