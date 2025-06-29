import os
import pandas as pd
from app.core.data_manager import DATA_DIR
from app.core.responsible_calendar_controller import asignar_base_responsable

FILE_PATH = os.path.join(DATA_DIR, "responsibles.csv")


def load_responsibles():
    if not os.path.exists(FILE_PATH):
        return []
    df = pd.read_csv(FILE_PATH)
    return df.to_dict("records")


def save_responsible(name, location, factory):
    df = pd.DataFrame([{
        "name": name,
        "location": location,
        "factory": factory
    }])
    if os.path.exists(FILE_PATH):
        existing_df = pd.read_csv(FILE_PATH)
        combined = pd.concat([existing_df, df], ignore_index=True)
    else:
        combined = df
    combined.drop_duplicates(subset=["name"], inplace=True)
    combined.to_csv(FILE_PATH, index=False)

    # Asignar calendario base automáticamente
    if location in ["Argentina", "EEUU", "China"]:
        asignar_base_responsable(name, location)


# ✅ ESTA FUNCIÓN VA AFUERA DEL BLOQUE ANTERIOR (misma indentación que `save_responsible`)
def delete_responsible_by_name(name):
    if not os.path.exists(FILE_PATH):
        return

    df = pd.read_csv(FILE_PATH)
    df = df[df["name"] != name]
    df.to_csv(FILE_PATH, index=False)

    # Eliminar también su calendario si existe
    from app.core.responsible_calendar_controller import cargar_calendarios_responsables, guardar_calendarios_responsables

    calendarios = cargar_calendarios_responsables()
    if name in calendarios:
        del calendarios[name]
        guardar_calendarios_responsables(calendarios)