class SessionStateHandler:
    DEFAULTS = {
        "task_to_delete": None,
        "confirm_delete": False,
        "project_to_delete": None,
        "confirm_delete_project": False,
        "editing_project": None,
        "current_project": None,
        "tasks": [],
        "task_changed": False,
        "custom_holidays": [],
        "calendar_dirty": False,
        "vista_general": None,
        "view_fake_project": False,
        "vista_proyecto": None,
        "imagenes_proyecto_bytes": [],
        "imagen_index": 0,
    }

    def __init__(self, session_state):
        self.state = session_state
        self.initialize_defaults()

    def initialize_defaults(self):
        for k, v in self.DEFAULTS.items():
            self.state.setdefault(k, v)