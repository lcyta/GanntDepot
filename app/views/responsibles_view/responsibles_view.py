import streamlit as st
from app.views.responsibles_view.responsibles_form import mostrar_formulario_alta
from app.views.responsibles_view.responsibles_list import mostrar_lista_responsables
from app.views.responsibles_view.editar_responsables_view import editar_responsable_view
from app.views.responsibles_view.mostrar_tareas_view_list import mostrar_tareas_view_list

def view_responsibles():
    mostrar_formulario_alta()
    mostrar_lista_responsables()
    editar_responsable_view()
    mostrar_tareas_view_list()

