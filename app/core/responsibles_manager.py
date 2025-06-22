import os
import pandas as pd
from app.core.data_manager import DATA_DIR

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