import streamlit as st
import pandas as pd
from datetime import date, timedelta

PAISES = ["Argentina", "EEUU", "China"]
KEY = "holiday_calendars"

# Feriados base precargados por país (pueden ser ampliados o importados desde un CSV/API)
FERIADOS_PREDETERMINADOS = {
    "Argentina": [
        date(2025, 1, 1),   # Año Nuevo
        date(2025, 3, 24),  # Día de la Memoria
        date(2025, 4, 2),   # Malvinas
        date(2025, 5, 25),  # Revolución de Mayo
        date(2025, 6, 20),  # Belgrano
    ],
    "EEUU": [
        date(2025, 1, 1),   # New Year's Day
        date(2025, 7, 4),   # Independence Day
        date(2025, 11, 27), # Thanksgiving
        date(2025, 12, 25), # Christmas
    ],
    "China": [
        date(2025, 2, 1),   # Chinese New Year (aproximado)
        date(2025, 5, 1),   # Labor Day
        date(2025, 10, 1),  # National Day
    ]
}

def show_country_holidays():
    st.markdown("### 📅 Ver feriados por país")

    # Inicializar el diccionario general si no está
    if KEY not in st.session_state:
        st.session_state[KEY] = {}

    # Inicializar cada país si no está, con sus feriados predeterminados
    for pais in PAISES:
        if pais not in st.session_state[KEY] or not st.session_state[KEY][pais]:
            st.session_state[KEY][pais] = FERIADOS_PREDETERMINADOS[pais][:]  # copiar para no modificar el original

    # Elegir país a visualizar
    pais_seleccionado = st.selectbox("🌎 Seleccioná un país", PAISES)

    feriados = st.session_state[KEY][pais_seleccionado]
    if feriados:
        df = pd.DataFrame(sorted(feriados), columns=["Fecha"])
        df["Día"] = df["Fecha"].apply(lambda x: x.strftime("%A"))
        st.dataframe(df, use_container_width=True)
    else:
        st.info(f"No hay feriados registrados para {pais_seleccionado}.")

def view_calendar():
    st.subheader("📆 Gestión de calendario laboral por país")

    # Inicializar estado si no existe
    if KEY not in st.session_state:
        st.session_state[KEY] = {pais: [] for pais in PAISES}

    pais = st.selectbox("🌎 Elegí un país", PAISES)

    ### ─── 1. Agregar feriado individual ───────────────
    st.markdown("#### ➕ Agregar feriado individual")
    fecha = st.date_input("Seleccioná una fecha", value=date.today(), key=f"feriado_individual_{pais}")
    if st.button("➕ Agregar feriado", key=f"btn_individual_{pais}"):
        if fecha not in st.session_state[KEY][pais]:
            st.session_state[KEY][pais].append(fecha)
            st.success(f"{fecha} agregado a {pais}")
        else:
            st.warning("Esa fecha ya está en el calendario.")

    ### ─── 2. Agregar feriado por rango ────────────────
    st.markdown("#### 📅 Agregar rango de feriados")
    rango = st.date_input("Rango de fechas", value=(date.today(), date.today() + timedelta(days=1)), key=f"rango_{pais}")
    if isinstance(rango, tuple) and len(rango) == 2:
        start, end = rango
        if st.button("➕ Agregar rango", key=f"btn_rango_{pais}"):
            nuevas = pd.date_range(start, end).to_pydatetime().tolist()
            nuevas_fechas = [f.date() for f in nuevas if f.date() not in st.session_state[KEY][pais]]
            st.session_state[KEY][pais].extend(nuevas_fechas)
            st.session_state[KEY][pais] = sorted(list(set(st.session_state[KEY][pais])))
            st.success(f"Rango agregado para {pais}: {start} a {end}")

    ### ─── 3. Mostrar feriados ────────────────────────
    feriados = st.session_state[KEY][pais]
    if feriados:
        st.markdown(f"#### 🗓️ Feriados en {pais}")
        df = pd.DataFrame(sorted(feriados), columns=["Fecha"])
        df["Día"] = df["Fecha"].apply(lambda x: x.strftime("%A"))
        st.dataframe(df, use_container_width=True)
    else:
        st.info(f"No hay feriados en {pais} aún.")

    st.markdown("#### 🔒 Sábados y domingos son no laborables")
    