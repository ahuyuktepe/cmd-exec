from app_runner.events.EventManager import EventManager
from app_runner.events.UIEventType import UIEventType
from app_runner.ui_elements.UIElement import UIElement


class UITextArea(UIElement):
    def __init__(self, id: str):
        super().__init__(id, 'textarea')

    # Event Listeners

    def displayText(self, data: dict = {}):
        self._printArea.printText(1, 1, data.get('text'))
        self.refresh()

    # Utility Methods

    def setListeners(self):
        EventManager.listenEvent(UIEventType.DISPLAY_TEXT, self)
