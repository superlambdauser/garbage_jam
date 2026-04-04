class EventBus:
    _listeners = {}

    @classmethod
    def on(cls, event, callback):
        if event not in cls._listeners:
            cls._listeners[event] = []
        cls._listeners[event].append(callback)
        print(f"registered: {event}, total listeners: {len(cls._listeners[event])}")

    @classmethod
    def off(cls, event, callback):
        if event in cls._listeners:
            cls._listeners[event].remove(callback)

    @classmethod
    def off_all(cls, owner):
        for event in cls._listeners:
            cls._listeners[event] = [cb for cb in cls._listeners[event] if cb.__self__ is not owner]

    @classmethod
    def emit(cls, event, **kwargs):
        for callback in cls._listeners.get(event, []):
            callback(**kwargs)