import streamlit as st

def render_reorder_ui(tasks):
    """Renderiza los controles de UI para reordenar tareas."""
    options = [f"{t.title} ({t.owner})" for t in tasks]
    mover_idx = st.selectbox(
        "🔀 Quiero mover:",
        range(len(options)),
        format_func=lambda i: options[i],
    )
    destino_idx = st.selectbox(
        "⬇️ Debajo de:",
        range(len(options)),
        format_func=lambda i: options[i],
        index=(mover_idx + 1) % len(tasks),
    )
    return mover_idx, destino_idx