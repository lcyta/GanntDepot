from app.core.calendar.services import set_base_responsable
from app.core.calendar.remove_holiday import remove_feriado_responsable
from app.core.calendar.add_holiday import add_feriado_responsable
from app.core.calendar.services_rango import add_rango_feriados_responsable
from app.core.calendar.remove_rango import remove_rango_feriados_responsable

from app.core.calendar.calendar_repository import (
    cargar_calendarios_responsables,
    guardar_calendarios_responsables,
)

# Este archivo actúa como controlador de alto nivel
# Ideal para llamarlo desde la vista o interfaz principal

def asignar_base_responsable(nombre, base):
    set_base_responsable(nombre, base)


def agregar_feriado_responsable(nombre, fecha, descripcion):
    add_feriado_responsable(nombre, fecha, descripcion)


def eliminar_feriado_responsable(nombre, fecha):
    remove_feriado_responsable(nombre, fecha)


def agregar_rango_feriados_responsable(nombre, fechas_con_nombre):
    add_rango_feriados_responsable(nombre, fechas_con_nombre)


def eliminar_rango_feriados_responsable(nombre, fechas):
    remove_rango_feriados_responsable(nombre, fechas)