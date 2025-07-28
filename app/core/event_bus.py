"""
Módulo para gestión simple de eventos tipo publish-subscribe (event bus).
Permite registrar callbacks (suscriptores) para eventos y publicar datos a esos eventos.
"""

subscribers = {}


def subscribe(event_name: str, callback):
    """
    Suscribe un callback a un evento específico.

    Parámetros:
        event_name (str): Nombre del evento al que se suscribe.
        callback (callable): Función que será llamada cuando se publique el evento.
    """
    subscribers.setdefault(event_name, []).append(callback)


def publish(event_name: str, data=None):
    """
    Publica un evento y llama a todos los callbacks suscritos, pasando datos.

    Parámetros:
        event_name (str): Nombre del evento a publicar.
        data (any, opcional): Datos que serán enviados a los callbacks.
    """
    for callback in subscribers.get(event_name, []):
        callback(data)
        