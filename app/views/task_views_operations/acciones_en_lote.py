import streamlit as st
from app.core.task.task_manager import save_all_tasks
from app.core.scheduler import adjust_task_schedule


def acciones_en_lote(tasks, project_name, responsibles_list):
    with st.expander("📦 Acciones en lote (Reasignar o Eliminar)", expanded=False):
        if not tasks:
            st.info("No hay tareas para mostrar.")
            return

        selected_tasks = []
        for i, task in enumerate(tasks):
            if st.checkbox(f"{task.title} ({task.owner})", key=f"select_task_{i}"):
                selected_tasks.append((i, task))

        if selected_tasks:
            st.markdown("### ✨ Acciones disponibles")

            col1, col2 = st.columns(2)

            # 🔁 Reasignar responsable
            new_owner = st.selectbox("Nuevo responsable", responsibles_list, key="mass_edit_owner")
            if col1.button("Reasignar tareas seleccionadas"):
                for _, task in selected_tasks:
                    task.owner = new_owner
                st.success(f"{len(selected_tasks)} tareas reasignadas a {new_owner}")
                save_all_tasks(project_name, adjust_task_schedule(tasks))
                st.rerun()  # ✅ actualizado

            # ❌ Eliminar seleccionadas
            if col2.button("Eliminar tareas seleccionadas"):
                indices_a_borrar = [i for i, _ in selected_tasks]
                for i in sorted(indices_a_borrar, reverse=True):
                    tasks.pop(i)
                st.success(f"{len(indices_a_borrar)} tareas eliminadas.")
                save_all_tasks(project_name, adjust_task_schedule(tasks))
                st.rerun()  # ✅ actualizado