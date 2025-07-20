import streamlit as st
import json
from app.core.holiday.manager_holiday_controller import inicializar_calendarios,cargar_feriados_predefinidos, KEY
from app.views.calendar.tabla_feriados import mostrar_tabla_feriados
from app.views.calendar.feriado_individual import gestionar_feriado_individual
from app.views.calendar.feriado_rango import gestionar_rango_feriados
from app.views.calendar.agregar_pais_calendario import vista_agregar_pais
from app.views.calendar.eliminar_pais import vista_eliminar_pais

def cargar_nombres_paises(path='data/feriados_predefinidos.json'):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return list(data.keys())
    except Exception as e:
        st.error(f"No se pudieron cargar los países: {e}")
        return []

def view_calendar():
    st.subheader("📆 Calendario laboral por país")

    # Si ya existe la sesión, forzamos la recarga de los feriados del archivo JSON
    if KEY in st.session_state:
        feriados_predef_actualizados = cargar_feriados_predefinidos()
        for pais, feriados in feriados_predef_actualizados.items():
            st.session_state[KEY][pais] = feriados
    else:
        inicializar_calendarios()

    nombres_paises = cargar_nombres_paises()
    if not nombres_paises:
        st.warning("No hay países disponibles para mostrar.")
        return

    pais_predeterminado = st.session_state.get("pais_seleccionado", nombres_paises[0])
    index_predeterminado = nombres_paises.index(pais_predeterminado) if pais_predeterminado in nombres_paises else 0

    pais = st.selectbox("🌍 Elegí un país", nombres_paises, index=index_predeterminado)

    mostrar_tabla_feriados(pais)
    with st.expander(" Gestion Feriados"):
        gestionar_feriado_individual(pais)
        gestionar_rango_feriados(pais)
    with st.expander("🌍 Gestion de calendarios"):
        vista_agregar_pais()
        vista_eliminar_pais(pais) 
