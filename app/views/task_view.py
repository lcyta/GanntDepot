import streamlit as st 
from app.core.responsibles_manager import load_responsibles
from app.core.task_manager import save_task, delete_task_by_index, save_all_tasks, load_tasks
from app.models.task import Task
from datetime import datetime, date
from app.core.scheduler import adjust_task_schedule

def safe_date(dt):
    if isinstance(dt, datetime):
        return dt.date()
    elif isinstance(dt, date):
        return dt
    else:
        try:
            return datetime.strptime(str(dt), "%Y-%m-%d").date()
        except:
            return None

def view_tasks(tasks, project_name):
    st.header("📋 Gestor de Tareas")
    tasks = load_tasks(project_name)
    responsibles = load_responsibles()
    responsibles_list = [r["name"] for r in responsibles] if responsibles else []

    if not responsibles_list:
        st.warning("⚠️ No hay responsables registrados. Por favor, agregá responsables antes de crear tareas.")

    # 📌 Crear nueva tarea
    with st.expander("➕ Crear nueva tarea", expanded=False):
        title = st.text_input("Título")
        owner = st.selectbox("Responsable", options=responsibles_list) if responsibles_list else None
        days = st.number_input("Duración (días)", min_value=1, step=1)

        if st.button("Agregar tarea"):
            if not title:
                st.error("El título es obligatorio.")
            elif not owner:
                st.error("Debés seleccionar un responsable.")
            else:
                task = Task(title, owner, days)
                save_task(task, project_name)
                st.session_state.task_changed = True
                st.rerun()

    # 🔧 Modificar tarea
    with st.expander("🔧 Modificar tarea", expanded=False):
        if not tasks:
            st.info("No hay tareas para modificar.")
        else:
            task_options = [f"{t.title} ({t.owner})" for t in tasks]
            selected_index = st.selectbox("Seleccioná una tarea", range(len(task_options)), format_func=lambda i: task_options[i])

            selected_task = tasks[selected_index]

            new_title = st.text_input("Nuevo título", value=selected_task.title, key="edit_title")
            new_owner = st.selectbox("Nuevo responsable", responsibles_list, index=responsibles_list.index(selected_task.owner), key="edit_owner")
            new_days = st.number_input("Nueva duración estimada (días)", value=selected_task.days, min_value=1, step=1, key="edit_days")

            col_mod, col_del = st.columns([1, 1])
            if col_mod.button("Modificar tarea"):
                selected_task.title = new_title
                selected_task.owner = new_owner
                selected_task.days = new_days

                updated_tasks = adjust_task_schedule(tasks)
                save_all_tasks(project_name, updated_tasks)

                st.success(f"Tarea modificada: {new_title}")
                st.session_state.task_changed = True
                st.rerun()

            if col_del.button("Eliminar tarea"):
                st.session_state.task_to_delete = selected_index
                st.session_state.confirm_delete = True
                st.rerun()

            if st.session_state.get("confirm_delete") and st.session_state.get("task_to_delete") == selected_index:
                st.warning(f"¿Confirmás eliminar la tarea **{selected_task.title}**?")
                c1, c2 = st.columns([1, 1])
                if c1.button("✔️ Sí", key="confirm_delete_task"):
                    delete_task_by_index(project_name, selected_index)
                    st.session_state.task_to_delete = None
                    st.session_state.confirm_delete = False
                    st.session_state.task_changed = True
                    st.success("Tarea eliminada.")
                    st.rerun()
                if c2.button("❌ No", key="cancel_delete_task"):
                    st.session_state.task_to_delete = None
                    st.session_state.confirm_delete = False
                    st.rerun()

    # 📑 Tareas existentes
    with st.expander("📑 Tareas existentes", expanded=True):
        if not tasks:
            st.info("No hay tareas todavía.")
        else:
            col1, col2, col3, col4, col5, col6 = st.columns([2.5, 2.5, 2, 2, 2, 2])
            col1.markdown("**Responsable**")
            col2.markdown("**Título**")
            col3.markdown("**Inicio**")
            col4.markdown("**Fin**")
            col5.markdown("**Duración real**")
            col6.markdown("**Duración estimada**")

            for task in tasks:
                start_date = safe_date(task.start)
                end_date = safe_date(task.end)

                duracion_real = (end_date - start_date).days + 1 if start_date and end_date else "N/A"
                duracion_estimada = task.days

                col1, col2, col3, col4, col5, col6 = st.columns([2.5, 2.5, 2, 2, 2, 2])
                col1.markdown(task.owner)
                col2.markdown(task.title)
                col3.markdown(str(start_date) if start_date else "Fecha inválida")
                col4.markdown(str(end_date) if end_date else "Fecha inválida")
                col5.markdown(f"{duracion_real} días" if duracion_real != "N/A" else "Inválido")
                col6.markdown(f"{duracion_estimada} días")

    # 🔀 Reordenar tareas
    with st.expander("🔀 Reordenar tareas", expanded=False):
        view_task_reorder(tasks, project_name)

def view_task_reorder(tasks, project_name):
    st.markdown("### 🔀 Reordenar tareas")

    if len(tasks) < 2:
        st.info("Necesitás al menos dos tareas para reordenar.")
        return

    options = [f"{t.title} ({t.owner})" for t in tasks]
    mover_idx = st.selectbox("🔀 Quiero mover:", range(len(options)), format_func=lambda i: options[i])
    destino_idx = st.selectbox("⬇️ Debajo de:", range(len(options)), format_func=lambda i: options[i], index=(mover_idx + 1) % len(tasks))

    if st.button("🔁 Reordenar tareas"):
        if mover_idx == destino_idx:
            st.warning("Seleccionaste la misma tarea.")
            return

        task_to_move = tasks.pop(mover_idx)
        tasks.insert(destino_idx, task_to_move)

        adjusted_tasks = adjust_task_schedule(tasks)
        save_all_tasks(project_name, adjusted_tasks)

        st.success(f"Tarea '{task_to_move.title}' movida correctamente debajo de '{tasks[destino_idx].title}'.")
        st.session_state.task_changed = True
        st.rerun()