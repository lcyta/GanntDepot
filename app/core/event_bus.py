subscribers = {}


def subscribe(event_name: str, callback):
    subscribers.setdefault(event_name, []).append(callback)


def publish(event_name: str, data=None):
    for callback in subscribers.get(event_name, []):
        callback(data)
