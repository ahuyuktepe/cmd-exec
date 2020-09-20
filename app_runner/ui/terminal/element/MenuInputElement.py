import curses

from app_runner.events.EventManager import EventManager
from app_runner.events.UIEventType import UIEventType
from app_runner.ui.terminal.element.UIElement import UIElement


class MenuInputElement(UIElement):
    __text: str

    def __init__(self, id: str):
        super().__init__(id, 'input')

    def setText(self, text: str):
        self.__text = text

    def print(self, data: dict = {}):
        self._window.addstr(self._y, self._x, self.__text)
        x = self._x + len(self.__text) + 1
        self.moveCursor(x, self._y)

    def listenUserInput(self):
        input = None
        while input != 'q':
            input = self._window.get_wch()
            if input == 'w':
                EventManager.triggerEvent(UIEventType.UP_KEY_PRESSED)
            elif input == 's':
                EventManager.triggerEvent(UIEventType.DOWN_KEY_PRESSED)
            elif input == 'a':
                EventManager.triggerEvent(UIEventType.LEFT_KEY_PRESSED)
            elif input == 'd':
                EventManager.triggerEvent(UIEventType.RIGHT_KEY_PRESSED)

    def exitListeningUserInput(self):
        curses.unget_wch('q')
