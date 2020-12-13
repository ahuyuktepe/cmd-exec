from app_runner.events.EventManager import EventManager
from app_runner.events.UIEventType import UIEventType
from app_runner.ui_elements.UIElement import UIElement


class UIText(UIElement):

    def __init__(self, id: str):
        super().__init__(id, 'text')
        self._y = 1

    # Utility Methods

    def display(self):
        self._printArea.printText(2, self._y, "Text")
        self.refresh()

    def setListeners(self):
        EventManager.listenEvent(UIEventType.UPDATE_TEXT, self)

    # Event Listeners

    def updateText(self, data: dict = {}):
        text = data.get('text')
        self._printArea.printText(1, self._y, text)
        self.clear()
        self.display()
        self.refresh()

