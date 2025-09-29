import streamlit as st
import pandas as pd
from app.core.responsibles_manager import load_responsibles
from app.core.calendar.feriado_service import get_feriados_for_owner
from app.utils.actions_registry import ACTIONS_RESPONSIBLE_CALENDAR
from app.utils.actions_executor import ejecutar_acciones_calendar

def view_responsible_calendar():
    with st.expander("📅 Calendario de feriados por responsable", expanded=False):

        responsables = load_responsibles()
        if not responsables:
            st.warning("No hay responsables registrados.")
            return

        nombres = [r["name"] for r in responsables]
        selected_name = st.selectbox("👤 Elegí un responsable", nombres)
        if not selected_name:
            return

        feriados = get_feriados_for_owner(selected_name)

        # 🔎 Mostrar feriados
        if feriados:
            st.subheader("📌 Lista de feriados")
            df = pd.DataFrame(feriados, columns=["Fecha", "Descripción"])
            # Opcional: formatear la fecha
            df["Fecha"] = df["Fecha"].apply(lambda d: d.strftime("%d/%m/%Y"))
            st.table(df)
        else:
            st.info("No hay feriados cargados para este responsable.")

        # ⚡ Obtener permisos desde session_state
        permissions = st.session_state.get("permissions", [])

        # Ejecutar acciones según permisos
        ejecutar_acciones_calendar(selected_name, feriados, permissions, ACTIONS_RESPONSIBLE_CALENDAR)