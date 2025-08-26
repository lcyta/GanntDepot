import os
import json
from pathlib import Path
import streamlit as st
import pandas as pd
from app.core.data_access.responsible_repository import ResponsibleRepository

# --- Carpeta y archivo de usuarios ---
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
USUARIOS_FILE = DATA_DIR / "usuarios_gestion.json"

# Inicializar archivo si no existe o está vacío
if not USUARIOS_FILE.exists() or USUARIOS_FILE.stat().st_size == 0:
    with open(USUARIOS_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, indent=4, ensure_ascii=False)

# --- Manejo de JSON ---
def load_usuarios():
    try:
        with open(USUARIOS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Si el archivo está corrupto o vacío
        return []

def save_usuarios(data):
    with open(USUARIOS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --- UI selección ---
def seleccionar_responsable_ui(responsibles):
    st.markdown("### 👤 Selecciona un Usuario")
    nombres = responsibles["name"].tolist()
    selected_name = st.selectbox("👤 Usuario", nombres)
    return responsibles[responsibles["name"] == selected_name].iloc[0].to_dict()

# --- Vista agregar usuarios ---
def view_users_add():
    with st.expander("➕ Agregar Usuarios", expanded=False):
        repo = ResponsibleRepository()
        responsibles_df = repo.load_all()
        if responsibles_df.empty:
            st.info("No hay responsables para agregar.")
            return

        selected = seleccionar_responsable_ui(responsibles_df)
        if not selected:
            return

        new_name = selected["name"]
        new_factory = selected["factory"]

        user_type = st.selectbox("🔐 Tipo de usuario", ["Admin", "Editor", "Solo lectura"], key=f"type_{new_name}")
        username = st.text_input("👤 Nombre de usuario (login)", key=f"user_{new_name}")
        password = st.text_input("🔑 Password", key=f"pass_{new_name}")

        view_users_permissions() 


        if st.button("💾 Guardar cambios", key=f"save_add_{new_name}"):
            usuarios = load_usuarios()

            # Validar duplicado
            if any(u["name"] == new_name for u in usuarios):
                st.error(f"Error: El responsable '{new_name}' ya tiene un usuario asignado.")
                return

            user_permissions = view_users_permissions()  # <-- Captura los permisos

            usuario_data = {
                "name": new_name,
                "factory": new_factory,
                "user_type": {
                    "role": user_type,
                    "permissions": user_permissions
                },
                "username": username,
                "password": password
            }
            usuarios.append(usuario_data)
            save_usuarios(usuarios)
            st.success(f"Usuario '{username}' agregado correctamente.")
            st.rerun()

# --- Vista tabla ---
def view_users_table():
    with st.expander("📋 Tabla de Usuarios", expanded=False):
        usuarios = load_usuarios()
        if not usuarios:
            st.info("No hay usuarios registrados.")
            return

        df = pd.DataFrame(usuarios)
        st.dataframe(df)

# --- Vista editar ---
def view_users_edit():
    with st.expander("✏️ Editar Usuario", expanded=False):
        usuarios = load_usuarios()
        if not usuarios:
            st.info("No hay usuarios registrados.")
            return

        df = pd.DataFrame(usuarios)
        selected_name = st.selectbox("👤 Selecciona el responsable a editar", df["name"].unique())
        selected_user = df[df["name"] == selected_name].iloc[0]

        user_type = st.selectbox("🔐 Tipo de usuario", ["Admin", "Editor", "Solo lectura"], index=["Admin", "Editor", "Solo lectura"].index(selected_user["user_type"]), key=f"edit_type_{selected_name}")
        username = st.text_input("👤 Nombre de usuario (login)", value=selected_user["username"], key=f"edit_user_{selected_name}")
        password = st.text_input("🔑 Password", value=selected_user["password"], key=f"edit_pass_{selected_name}")

        if st.button("💾 Guardar cambios", key=f"save_edit_{selected_name}"):
            for i, u in enumerate(usuarios):
                if u["name"] == selected_name:
                    usuarios[i]["username"] = username
                    usuarios[i]["password"] = password
                    usuarios[i]["user_type"] = user_type
                    break
            save_usuarios(usuarios)
            st.success(f"Usuario '{username}' actualizado correctamente.")
            st.rerun()

# --- Vista principal ---
def view_main_users():
    with st.expander("💻 Usuarios", expanded=False):
        view_users_add()
        view_users_table()
        view_users_edit()

def view_users_permissions():
    permisos = []

    gestionar_tareas = st.checkbox("📑 Gestionar Tareas")
    if gestionar_tareas:
        permisos.append("gestionar_tareas")  # Permiso general

        st.markdown("##### ➝ Subpermisos de Gestión de Tareas")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("**Acción**")
        with col2:
            st.markdown("**Ver**")

        acciones = [
            ("crear_tarea", "➕ Crear nueva tarea"),
            ("modificar_tarea", "🔧 Modificar tarea"),
            ("reordenar_tareas", "🔀 Reordenar tareas"),
            ("acciones_lote", "📦 Acciones en lote"),
            ("ver_tareas", "📑 Tareas existentes"),
        ]

        for key, label in acciones:
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(label)
            with col2:
                checked = st.checkbox(" ", key=f"{key}_ver", label_visibility="collapsed")
                if checked:
                    permisos.append(key)

    return permisos