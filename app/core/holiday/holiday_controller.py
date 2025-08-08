from app.core.holiday.holiday_service import obtener_feriados
from app.core.holiday.holiday_add import agregar_feriado
from app.core.holiday.holiday_delete import eliminar_feriado

class HolidayController:
    def __init__(self, pais):
        self.pais = pais

    def obtener_feriados(self):
        return obtener_feriados(self.pais)

    def agregar_feriado(self, fecha, descripcion):
        descripcion = descripcion.strip()
        if not descripcion:
            return False, "Debe ingresar una descripción del feriado."
        agregado = agregar_feriado(self.pais, fecha, descripcion)
        if not agregado:
            return False, "El feriado ya existe para esa fecha."
        return True, "Feriado agregado."

    def eliminar_feriado(self, feriados, seleccionado):
        fecha_a_borrar = [
            f for f, desc in feriados if f"{f.strftime('%Y-%m-%d')} - {desc}" == seleccionado
        ]
        if not fecha_a_borrar:
            return False, "No se encontró el feriado seleccionado."
        eliminar_feriado(self.pais, fecha_a_borrar[0])
        return True, "Feriado eliminado."