import random
from datetime import datetime, timedelta

def generar_datos_iniciales(projects):
    localidades = ["Buenos Aires", "Córdoba", "Rosario", "Mendoza", "La Plata", "Salta"]
    clientes = ["Cliente A", "Cliente B", "Cliente C", "Cliente D"]
    estados = ["En progreso", "Finalizado", "Pendiente"]
    responsables = ["Juan", "Ana", "Luis", "Marta", "Carlos", "Lucía", "Pedro", "Sofía"]

    datos = []
    for nombre in projects:
        datos.append({
            "Proyecto": nombre,
            "Cliente": random.choice(clientes),
            "Responsable": random.choice(responsables),
            "Localidad": random.choice(localidades),
            "Metros²": random.randint(100, 2000),
            "Inicio": (datetime.today() - timedelta(days=random.randint(10, 100))).date(),
            "Duración estimada (días)": random.choice([60, 90, 120]),
            "Estado": random.choice(estados)
        })
    return {item["Proyecto"]: item for item in datos}