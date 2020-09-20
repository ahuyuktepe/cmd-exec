
class EventManager:
    __bindings: dict = {}

    @staticmethod
    def bindEvent(evntId: str, obj: object):
        binding = EventManager.__bindings.get(evntId)
        if binding is None:
            EventManager.__bindings[evntId] = []
        EventManager.__bindings[evntId].append(obj)

    @staticmethod
    def removeBinding(evntId: str):
        if EventManager.__bindings.get(evntId) is not None:
            del EventManager.__bindings[evntId]

    @staticmethod
    def clearBindings():
        EventManager.__bindings.clear()

    @staticmethod
    def triggerEvent(evntId: str, data: dict = {}):
        bindings: list = EventManager.__bindings.get(evntId)
        if bindings is not None:
            for binding in bindings:
                func = getattr(binding, evntId)
                func(data)
