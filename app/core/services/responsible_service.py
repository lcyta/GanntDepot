import pandas as pd
from app.core.data_access.responsible_repository import ResponsibleRepository
from app.core.calendar.calendar_service import CalendarService

class ResponsibleService:
    def __init__(self,
                 repository: ResponsibleRepository = None,
                 calendar_service: CalendarService = None):
        self.repository = repository or ResponsibleRepository()
        self.calendar_service = calendar_service or CalendarService()

    def load_responsibles(self):
        df = self.repository.load_all()
        return df.to_dict("records")

    def save_responsible(self, name: str, location: str, factory: str):
        df = self.repository.load_all()
        df_new = pd.DataFrame([{"name": name, "location": location, "factory": factory}])
        df_combined = pd.concat([df, df_new], ignore_index=True)
        df_combined.drop_duplicates(subset=["name"], inplace=True)
        self.repository.save_all(df_combined)
        self.calendar_service.assign_base_if_needed(name, location)

    def delete_responsible_by_name(self, name: str):
        df = self.repository.load_all()
        df = df[df["name"] != name]
        self.repository.save_all(df)
        self.calendar_service.remove_calendar_if_exists(name)

    def update_responsible(self, name: str, new_location: str, new_factory: str):
        df = self.repository.load_all()
        if name not in df["name"].values:
            return
        df.loc[df["name"] == name, "location"] = new_location
        df.loc[df["name"] == name, "factory"] = new_factory
        self.repository.save_all(df)
        self.calendar_service.assign_base_if_needed(name, new_location)

    def update_responsible_name(self, old_name: str, new_name: str, new_location: str, new_factory: str):
        df = self.repository.load_all()
        if old_name not in df["name"].values:
            return
        df.loc[df["name"] == old_name, "name"] = new_name
        df.loc[df["name"] == new_name, "location"] = new_location
        df.loc[df["name"] == new_name, "factory"] = new_factory
        df.drop_duplicates(subset=["name"], keep="last", inplace=True)
        self.repository.save_all(df)
        self.calendar_service.assign_base_if_needed(new_name, new_location)
        if old_name != new_name:
            self.calendar_service.remove_calendar_if_exists(old_name)