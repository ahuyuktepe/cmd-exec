from app_runner.ui.terminal.element.UIElement import UIElement
from app_runner.utils.DictUtil import DictUtil


class EventManager:
    __listeners: dict = {}

    @staticmethod
    def listenEvent(eid: str, element: UIElement):
        binding = EventManager.__listeners.get(eid)
        if binding is None:
            EventManager.__listeners[eid] = []
        EventManager.__listeners[eid].append(element)

    @staticmethod
    def removeListenersByElementId(id: str):
        elements: list
        element: UIElement
        for key, elements in EventManager.__listeners:
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
    def triggerEventByElementId(evntId: str, elementId: str, data: dict = {}):
        listeners: list = EventManager.__listeners.get(evntId)
        if listeners is not None:
            listener: UIElement
            for listener in listeners:
                if listener.getId() == elementId:
                    func = getattr(listener, evntId)
                    func(data)
