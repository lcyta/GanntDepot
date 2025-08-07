'''
from data.responsible_repository import (
    load_responsibles_df,
    save_responsibles_df
)
from app.core.calendar.calendar_updater import (
    asignar_base_responsable,
    cargar_calendarios_responsables,
    guardar_calendarios_responsables,
)

class ResponsibleService:
    def get_all(self):
        df = load_responsibles_df()
        return df.to_dict("records")

    def save(self, name, location, factory):
        df = load_responsibles_df()
        df_new = {"name": name, "location": location, "factory": factory}
        df = pd.concat([df, pd.DataFrame([df_new])], ignore_index=True)
        df.drop_duplicates(subset=["name"], inplace=True)
        save_responsibles_df(df)

        if location in ["Argentina", "EEUU", "China"]:
            asignar_base_responsable(name, location)

    def delete(self, name):
        df = load_responsibles_df()
        df = df[df["name"] != name]
        save_responsibles_df(df)

        calendarios = cargar_calendarios_responsables()
        if name in calendarios:
            del calendarios[name]
            guardar_calendarios_responsables(calendarios)

    def update(self, name, new_location, new_factory):
        df = load_responsibles_df()
        if name not in df["name"].values:
            return
        df.loc[df["name"] == name, "location"] = new_location
        df.loc[df["name"] == name, "factory"] = new_factory
        save_responsibles_df(df)

        if new_location in ["Argentina", "EEUU", "China"]:
            asignar_base_responsable(name, new_location)

    def rename(self, old_name, new_name, new_location, new_factory):
        df = load_responsibles_df()
        if old_name not in df["name"].values:
            return

        df.loc[df["name"] == old_name, "name"] = new_name
        df.loc[df["name"] == new_name, "location"] = new_location
        df.loc[df["name"] == new_name, "factory"] = new_factory
        df.drop_duplicates(subset=["name"], keep="last", inplace=True)
        save_responsibles_df(df)

        if new_location in ["Argentina", "EEUU", "China"]:
            asignar_base_responsable(new_name, new_location)

        if old_name != new_name:
            calendarios = cargar_calendarios_responsables()
            if old_name in calendarios:
                del calendarios[old_name]
                guardar_calendarios_responsables(calendarios)
                '''