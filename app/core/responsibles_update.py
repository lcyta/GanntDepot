from app.core.data_access.responsible_repository import ResponsibleRepository
from app.core.calendar.calendar_service import CalendarService

_repo = ResponsibleRepository()
_calendar = CalendarService()

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