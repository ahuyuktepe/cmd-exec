from app_runner.events.EventManager import EventManager
from app_runner.events.UIEventType import UIEventType
from app_runner.ui_elements.UIElement import UIElement


class UIText(UIElement):
    __lineCount: int
    __lines: list

    def __init__(self, id: str):
        super().__init__(id, 'text')
        self._y = 0
        self.__lines = []

    # Utility Methods

    def display(self):
        super(UIText, self).display()
        self.__lineCount = self.getHeight() - 2

    # Event Listeners

    def appendText(self, data: dict = {}):
        self.clear()
        text = data.get('text')
        if self._y == self.__lineCount:
            self.__scrollUp()
        else:
            self._y += 1
        self._printArea.printText(1, self._y, text)
        self.refresh()

    # Private Methods

    def upKeyPressed(self, data):
        print('UIText: upKeyPressed')
