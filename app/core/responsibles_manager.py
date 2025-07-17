import os
import pandas as pd
from app.core.data_manager import DATA_DIR
from app.core.calendar.calendar_updater import (
    asignar_base_responsable,
    cargar_calendarios_responsables,
    guardar_calendarios_responsables,
)

FILE_PATH = os.path.join(DATA_DIR, "responsibles.csv")


def load_responsibles():
    if not os.path.exists(FILE_PATH):
        return []
    df = pd.read_csv(FILE_PATH)
    return df.to_dict("records")


def save_responsible(name, location, factory):
    df_new = pd.DataFrame(
        [
            {"name": name,
             "location": location,
              "factory": factory
            }
        ]
    )
    if os.path.exists(FILE_PATH):
        df_existing = pd.read_csv(FILE_PATH)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new

    df_combined.drop_duplicates(subset=["name"], inplace=True)
    df_combined.to_csv(FILE_PATH, index=False)

    if location in ["Argentina", "EEUU", "China"]:
        asignar_base_responsable(name, location)


def delete_responsible_by_name(name):
    if not os.path.exists(FILE_PATH):
        return

    df = pd.read_csv(FILE_PATH)
    df = df[df["name"] != name]
    df.to_csv(FILE_PATH, index=False)

    calendarios = cargar_calendarios_responsables()
    if name in calendarios:
        del calendarios[name]
        guardar_calendarios_responsables(calendarios)

def update_responsible(name, new_location, new_factory):
    if not os.path.exists(FILE_PATH):
        return

    df = pd.read_csv(FILE_PATH)

    # Si el nombre no existe, no se actualiza nada
    if name not in df["name"].values:
        return

    df.loc[df["name"] == name, "location"] = new_location
    df.loc[df["name"] == name, "factory"] = new_factory
    df.to_csv(FILE_PATH, index=False)

    # También actualizamos los calendarios si corresponde
    if new_location in ["Argentina", "EEUU", "China"]:
        asignar_base_responsable(name, new_location)

def update_responsible_name(old_name, new_name, new_location, new_factory):
    if not os.path.exists(FILE_PATH):
        return

    df = pd.read_csv(FILE_PATH)

    if old_name not in df["name"].values:
        return

    df.loc[df["name"] == old_name, "name"] = new_name
    df.loc[df["name"] == new_name, "location"] = new_location
    df.loc[df["name"] == new_name, "factory"] = new_factory

    # Eliminar duplicados si el nuevo nombre ya existía
    df.drop_duplicates(subset=["name"], keep="last", inplace=True)

    df.to_csv(FILE_PATH, index=False)

    # Actualizar calendario si aplica
    if new_location in ["Argentina", "EEUU", "China"]:
        asignar_base_responsable(new_name, new_location)

    # Si el nombre cambió, eliminar calendario viejo
    if old_name != new_name:
        calendarios = cargar_calendarios_responsables()
        if old_name in calendarios:
            del calendarios[old_name]
            guardar_calendarios_responsables(calendarios)