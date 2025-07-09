from datetime import date

FERIADOS_PREDETERMINADOS = {
    "Argentina": [
        (date(2025, 1, 1), "Año Nuevo"),
        (date(2025, 3, 24), "Día de la Memoria"),
        (date(2025, 4, 2), "Malvinas"),
        (date(2025, 5, 25), "Revolución de Mayo"),
        (date(2025, 6, 20), "Paso a la Inmortalidad de Belgrano"),
    ],
    "EEUU": [
        (date(2025, 1, 1), "New Year's Day"),
        (date(2025, 7, 4), "Independence Day"),
        (date(2025, 11, 27), "Thanksgiving"),
        (date(2025, 12, 25), "Christmas"),
    ],
    "China": [
        (date(2025, 2, 1), "Año Nuevo Chino (aproximado)"),
        (date(2025, 5, 1), "Día del Trabajo"),
        (date(2025, 10, 1), "Día Nacional de China"),
    ],
}
