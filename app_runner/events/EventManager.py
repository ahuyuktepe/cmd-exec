from app_runner.ui.terminal.element.UIElement import UIElement


class EventManager:
    __listeners: dict = {}

    @staticmethod
    def listenEvent(eid: str, element: UIElement):
        bindings = EventManager.__listeners.get(eid)
        if bindings is None:
            EventManager.__listeners[eid] = [element]
        elif not EventManager.__isElementListeningEvent(eid, element.getId()):
            EventManager.__listeners[eid].append(element)

    @staticmethod
    def removeListenersByElementId(id: str):
        elements: list
        element: UIElement
        for key, elements in EventManager.__listeners.items():
            for element in elements:
                if element.getId() == id:
                    del element

    @staticmethod
    def clearListeners():
        EventManager.__listeners.clear()

    @staticmethod
    def triggerEvent(eid: str, data: dict = {}):
        listeners: list = EventManager.__listeners.get(eid)
        if listeners is not None:
            for listener in listeners:
                func = getattr(listener, eid)
                func(data)

    @staticmethod
    def triggerEventByElementId(eid: str, elementId: str, data: dict = {}):
        listeners: list = EventManager.__listeners.get(eid)
        if listeners is not None:
            listener: UIElement
            for listener in listeners:
                print('id: ' + listener.getId())
                if listener.getId() == elementId:
                    func = getattr(listener, eid)
                    func(data)

    @staticmethod
    def __isElementListeningEvent(evntId: str, elementId: str):
        bindings = EventManager.__listeners.get(evntId)
        if bindings is None:
            return False
        for element in bindings:
            if element.getId() == elementId:
                return True
        return False
