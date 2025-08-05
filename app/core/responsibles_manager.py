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

def update_responsible(name, new_location, new_factory):
    df = _repo.load_all()
    if name not in df["name"].values:
        return
    df.loc[df["name"] == name, ["location", "factory"]] = [new_location, new_factory]
    _repo.save_all(df)
    _calendar.assign_base_if_needed(name, new_location)

def update_responsible_name(old_name, new_name, new_location, new_factory):
    df = _repo.load_all()
    if old_name not in df["name"].values:
        return
    df.loc[df["name"] == old_name, ["name", "location", "factory"]] = [new_name, new_location, new_factory]
    df.drop_duplicates(subset=["name"], keep="last", inplace=True)
    _repo.save_all(df)
    _calendar.assign_base_if_needed(new_name, new_location)
    if old_name != new_name:
        _calendar.remove_calendar_if_exists(old_name)