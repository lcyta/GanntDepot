import streamlit as st

def mostrar_filtros(df):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        f_proyecto = st.selectbox("Proyecto", ["Todos"] + sorted(df["Proyecto"].unique().tolist()))
    with col2:
        f_responsable = st.selectbox("Responsable", ["Todos"] + sorted(df["Responsable"].unique().tolist()))
    with col3:
        f_estado = st.selectbox("Estado", ["Todos"] + sorted(df["Estado"].dropna().unique().tolist()))
    with col4:
        f_factory = st.selectbox("Fábrica/Sede", ["Todos"] + sorted(df["Fábrica/Sede"].unique().tolist()))
    return f_proyecto, f_responsable, f_estado, f_factory


def aplicar_filtros(df, proyecto, responsable, estado, factory):
    df_filtrado = df.copy()
    if proyecto != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Proyecto"] == proyecto]
    if responsable != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Responsable"] == responsable]
    if estado != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Estado"] == estado]
    if factory != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Fábrica/Sede"] == factory]
    return df_filtrado