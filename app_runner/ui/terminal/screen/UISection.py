import curses
from app_runner.ui.terminal.element.UIElement import UIElement
from app_runner.ui.terminal.element.UIMenuElement import UIMenuElement


class UISection(UIElement):
    _window: object
    _elements: dict

    def __init__(self, sid: str, sType: str):
        super().__init__(sid, sType)
        self._elements = {}

    def initialize(self):
        self._window = curses.newwin(self._height, self._width, self._y, self._x)

    # Setter Methods

    def addBorder(self):
        self._window.border()

    def addElement(self, element: UIElement):
        if element is not None:
            self._elements[element.getId()] = element

    def setActiveMenuElement(self, element: UIMenuElement):
        self._elements['active_menu'] = element

    def getUserInput(self) -> str:
        curses.curs_set(1)
        self.moveCursor(2, 1)
        self._window.clrtoeol()
        return self._window.getstr().decode('utf-8')

    # Utility Methods

    def print(self):
        self.addBorder()
        element: UIElement
        for key, element in self._elements.items():
            element.print(self._window)
        self.refresh()

    def clear(self):
        self._window.clear()

    def refresh(self):
        self._window.refresh()

    def moveCursor(self, x: int, y: int):
        self._window.move(y, x)


