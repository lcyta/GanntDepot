import os
import pandas as pd
from app.core.data_manager import DATA_DIR

FILE_PATH = os.path.join(DATA_DIR, "responsibles.csv")

class ResponsibleRepository:
    def __init__(self, file_path=FILE_PATH):
        self.file_path = file_path

    def exists(self):
        return os.path.exists(self.file_path)

    def load_all(self):
        if not self.exists():
            return pd.DataFrame(columns=["name", "location", "factory"])
        return pd.read_csv(self.file_path)

    def save_all(self, df):
        df.to_csv(self.file_path, index=False)