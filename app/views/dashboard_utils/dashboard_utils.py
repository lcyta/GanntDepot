def sync_project_selection(controller, selected_project):
    if selected_project != controller.state.current_project:
        controller.select_project(selected_project)
        controller.state.task_changed = False
        controller.state.calendar_dirty = False
    elif controller.state.calendar_dirty and selected_project:
        controller.reload_tasks()
        controller.state.calendar_dirty = False
