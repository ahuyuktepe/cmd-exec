import curses

from app_runner.ui.terminal.element.LabelUIElement import LabelUIElement
from app_runner.ui.terminal.element.UIElement import UIElement


class UISection(UIElement):
    _title: str
    _window: object
    _elements: dict = {}

    def __init__(self, sid: str, sType: str, title: str = None):
        super().__init__(sid, sType)
        self._title = title

    def initialize(self):
        self._window = curses.newwin(self._height, self._width, self._y, self._x)

    def printBorder(self):
        self._window.border()

    def refresh(self):
        self._window.refresh()

    def addElement(self, element: UIElement):
        if element is not None:
            self._elements[element.getId()] = element

    def getTitle(self) -> str:
        return self._title

    def print(self):
        self.printBorder()
        self.printElements()
        self.refresh()

    def printElements(self):
        element: UIElement
        for key, element in self._elements.items():
            if isinstance(element, LabelUIElement):
                self.__printLabelElement(element)

    def __printLabelElement(self, element: LabelUIElement):
        self._window.addstr(element.getY(), element.getX(), element.getText(), curses.color_pair(1))
