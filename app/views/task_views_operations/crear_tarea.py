import streamlit as st
from app.models.task import Task
from app.core.task.task_manager import save_task

# ───── 1️⃣ Inicializar contador ─────
def inicializar_contador_tarea():
    if "crear_tarea_counter" not in st.session_state:
        st.session_state.crear_tarea_counter = 0
    return st.session_state.crear_tarea_counter

# ───── 2️⃣ Renderizar formulario ─────
def renderizar_formulario_tarea(c, responsibles_list):
    title = st.text_input("📌 Título de Tarea", key=f"title_{c}")
    owner_options = [""] + responsibles_list if responsibles_list else [""]
    owner = st.selectbox("👤 Responsable", options=owner_options, key=f"owner_{c}")
    days = st.number_input("⏱️ Duración estimada (días)", min_value=1, step=1, key=f"days_{c}")
    tipo = st.text_input("📝 Tipo de Tarea", key=f"tipo_{c}")
    riesgo = st.selectbox("⚠️ Riesgo", options=["Bajo", "Medio", "Alto"], key=f"riesgo_{c}")
    estado = st.selectbox("⏳ Estado", options=["En curso", "Terminado", "En Espera"], key=f"estado_{c}")
    return title, owner, days, tipo, riesgo, estado

# ───── 3️⃣ Validar inputs ─────
def validar_tarea(title, owner):
    if not title:
        return "El título es obligatorio."
    if not owner:
        return "Debés seleccionar un responsable."
    return None

# ───── 4️⃣ Crear y guardar tarea ─────
def crear_y_guardar_tarea(title, owner, days, tipo, riesgo, estado, project_name):
    task = Task(
        title=title,
        owner=owner,
        days=days,
        tipo=tipo,
        riesgo=riesgo,
        estado=estado,
    )
    save_task(task, project_name)
    st.success(f"Tarea creada: {title}")
    st.session_state.task_changed = True
    st.session_state.crear_tarea_counter += 1
    st.rerun()

# ───── 5️⃣ Función principal ─────
def crear_nueva_tarea(project_name, responsibles_list):
    c = inicializar_contador_tarea()

    with st.expander("➕ Crear nueva tarea", expanded=False):
        title, owner, days, tipo, riesgo, estado = renderizar_formulario_tarea(c, responsibles_list)

        if st.button("Agregar tarea", key=f"btn_{c}"):
            error = validar_tarea(title, owner)
            if error:
                st.error(error)
            else:
                crear_y_guardar_tarea(title, owner, days, tipo, riesgo, estado, project_name)