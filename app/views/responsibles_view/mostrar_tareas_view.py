import streamlit as st
from app.views.responsibles_view.responsibles_form import mostrar_formulario_alta
from app.views.responsibles_view.responsibles_list import mostrar_lista_responsables
from app.views.responsibles_view.editar_responsables_view import editar_responsable_view
from print_tareas_todos import mostrar_tareas_todos_proyectos


# =========================
# Funciones auxiliares
# =========================
def mostrar_duracion_proyecto(duracion_total):
    """Muestra el rango de fechas y duración total del proyecto."""
    inicio, fin, rango_dias = duracion_total
    if inicio and fin:
        st.success(
            f"Duración total del proyecto: {rango_dias} días "
            f"({inicio.date()} → {fin.date()})"
        )


def mostrar_proyecto(proyecto, info):
    """Renderiza la información de un único proyecto."""
    with st.container():
        st.write(f"### 📌 Proyecto: {proyecto}")

        if info is None or info["df"] is None or info["df"].empty:
            st.info("No hay tareas válidas")
            return

        # Mostrar tabla de tareas
        st.dataframe(info["df"])

        # Mostrar duración total
        mostrar_duracion_proyecto(info["duracion_total"])


# =========================
# Vista principal
# =========================
def mostrar_tareas_view():
    """Vista que muestra todas las tareas agrupadas por proyecto."""
    with st.expander("📂 Tareas de todos los proyectos", expanded=False):
        resultados = mostrar_tareas_todos_proyectos()

        for proyecto, info in resultados.items():
            mostrar_proyecto(proyecto, info)
            