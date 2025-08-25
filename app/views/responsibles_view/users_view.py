import streamlit as st
import json
from pathlib import Path
from app.core.holiday_data import FERIADOS_PREDETERMINADOS
from app.core.data_access.responsible_repository import ResponsibleRepository

USUARIOS_FILE = Path("usuarios_gestion.json")

# --- Manejo de usuarios JSON ---
def load_usuarios():
    if USUARIOS_FILE.exists():
        with open(USUARIOS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_usuarios(data):
    with open(USUARIOS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# --- UI selección ---
def seleccionar_responsable_ui(responsibles):
    st.markdown("### 👤 Selecciona un Usuario")
    nombres = responsibles["name"].tolist()
    selected_name = st.selectbox("👤 Usuario", nombres)
    return responsibles[responsibles["name"] == selected_name].iloc[0].to_dict()


# --- Formulario ---
def formulario_edicion_responsable(selected):
    st.markdown("### 🔧 Editar Usuario")

    new_name = st.text_input(
        "👤 Nuevo nombre", 
        value=selected["name"], 
        key=f"name_{selected['name']}"
    )

    # Países desde feriados
    country_list = list(FERIADOS_PREDETERMINADOS.keys())
    pais_predeterminado = selected.get("location", country_list[0] if country_list else "")
    index_predeterminado = country_list.index(pais_predeterminado) if pais_predeterminado in country_list else 0

    new_location = st.selectbox(
        "🌍 Nuevo país", 
        country_list, 
        index=index_predeterminado, 
        key=f"location_{selected['name']}"
    )

    # Fábrica
    st.caption(f"🏭 Fábrica actual: **{selected['factory']}**")
    new_factory = st.text_input(
        "✍️ Nueva fábrica", 
        value=selected["factory"], 
        key=f"factory_{selected['name']}"
    )

    # Tipo de usuario
    user_type = st.selectbox(
        "🔐 Tipo de usuario", 
        ["Admin", "Editor", "Solo lectura"], 
        key=f"type_{selected['name']}"
    )

    # Usuario y password
    username = st.text_input(
        "👤 Nombre de usuario (login)", 
        value=selected.get("username", ""), 
        key=f"user_{selected['name']}"
    )

    password = st.text_input(
        "🔑 Password", 
        type="password", 
        value=selected.get("password", ""), 
        key=f"pass_{selected['name']}"
    )

    return new_name, new_location, new_factory, user_type, username, password

def view_users_list():
    '''st.subheader("📝 Gestión de Usuarios")

    projects = load_projects()
    if not projects:
        st.info("No hay proyectos creados todavía.")
        return

    mostrar_tabla_proyectos(projects)
    selected_project = mostrar_detalles_proyecto(projects)
    editar_eliminar_proyectos(projects)
    mostrar_tareas_view()
    render_all_shipments()
    #if selected_project:
     #   render_project_image_uploader(selected_project)
     '''
    with st.expander("✉️ Usuarios", expanded=False):
        repo = ResponsibleRepository()
        responsibles_df = repo.load_all()

        if responsibles_df.empty:
            st.info("No hay responsables para editar.")
            return

        selected = seleccionar_responsable_ui(responsibles_df)
        if not selected:
            return

        new_name, new_location, new_factory, user_type, username, password = formulario_edicion_responsable(selected)

        if st.button("💾 Guardar cambios"):
            usuarios = load_usuarios()

            # Si no existe el país todavía en JSON, lo creamos
            if new_location not in usuarios:
                usuarios[new_location] = []

            # Buscar si ya existe usuario con ese username en esa location
            usuarios[new_location] = [
                u for u in usuarios[new_location] if u.get("username") != username
            ]

            # Agregar/Actualizar usuario
            usuario_data = {
                "name": new_name,
                "factory": new_factory,
                "user_type": user_type,
                "username": username,
                "password": password
            }
            usuarios[new_location].append(usuario_data)

            save_usuarios(usuarios)

            st.success(f"Usuario '{username}' actualizado en {USUARIOS_FILE}.")
            st.rerun()