def ejecutar_acciones_permitidas(tasks, project_name, responsibles_list, permissions, actions):
    for grupo_cfg in actions.values():
        for sub_key, sub_cfg in grupo_cfg.get("subacciones", {}).items():
            if sub_key in permissions and "action" in sub_cfg:
                sub_cfg["action"](tasks, project_name, responsibles_list)


def ejecutar_acciones_proyecto(detalle_proyecto, permissions, actions):
    for grupo_cfg in actions.values():
        for sub_key, sub_cfg in grupo_cfg.get("subacciones", {}).items():
            if sub_key in permissions and "action" in sub_cfg:
                sub_cfg["action"](detalle_proyecto)