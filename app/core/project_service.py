def get_all_project_data(projects, session_data):
    return [session_data[n] for n in projects if n in session_data]

def update_project_data(name, data, session_data):
    session_data[name] = data