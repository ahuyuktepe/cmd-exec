from app_runner.ui_elements.UIElement import UIElement
from app_runner.utils.ObjUtil import ObjUtil


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
    def listenEvents(eids: list, element: UIElement):
        for eid in eids:
            EventManager.listenEvent(eid, element)

    @staticmethod
    def removeListenersByElementId(id: str, ignoreEventTypes: list = []):
        for eventType, elements in EventManager.__listeners.items():
            for i in range(len(elements)):
                element = elements[i]
                if element.getId() == id and eventType not in ignoreEventTypes :
                    del elements[i]

    @staticmethod
    def removeListenersForElement(id: str, eventTypes: list = []):
        for eventType, elements in EventManager.__listeners.items():
            for i in range(len(elements)):
                element = elements[i]
                if element.getId() == id and eventType in eventTypes:
                    del elements[i]

    @staticmethod
    def clearListeners():
        EventManager.__listeners.clear()

    @staticmethod
    def triggerEvent(eid: str, data: dict = {}):
        listeners: list = EventManager.__listeners.get(eid)
        if listeners is not None:
            for listener in listeners:
                if ObjUtil.hasMethod(listener, eid):
                    func = getattr(listener, eid)
                    func(data)

    @staticmethod
    def triggerEventByElementId(eid: str, elementId: str, data: dict = {}):
        listeners: list = EventManager.__listeners.get(eid)
        if listeners is not None:
            listener: UIElement
            for listener in listeners:
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
