import curses
from app_runner.ui.terminal.element.UIElement import UIElement


class UISection(UIElement):
    __elements: list
    __withBorder: bool

    def __init__(self, sid: str, withBorder: bool):
        super().__init__(sid, 'section')
        self.__elements = []
        self.__withBorder = withBorder

    def initialize(self):
        self._window = curses.newwin(self._height, self._width, self._y, self._x)

    def print(self, data: dict = {}):
        element: UIElement
        for element in self.__elements:
            element.print(data)
        if self.__withBorder:
            self.addBorder()
        self.refresh()

    def addElement(self, element: UIElement):
        if element is not None:
            self.__elements.append(element)

    def getElementByType(self, type: str) -> UIElement:
        for element in self.__elements:
            if element.getType() == type:
                return element
        return None

    def clear(self):
        element: UIElement
        for element in self.__elements:
            element.clear()
        self.refresh()
