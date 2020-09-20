import curses
from app_runner.ui.terminal.element.UIElement import UIElement
from app_runner.ui.terminal.element.UISection import UISection


class UIView(UIElement):
    __sections: list

    def __init__(self, id: str):
        super().__init__(id, 'screen')
        self.__sections = []

    def initialize(self):
        self._window = curses.initscr()
        curses.cbreak()
        curses.noecho()
        self._window.nodelay(True)
        self._x = 0
        self._y = 0
        self._height, self._width = self._window.getmaxyx()

    def addSection(self, section: UISection):
        if section is not None:
            self.__sections.append(section)

    def print(self, data: dict = {}):
        section: UISection
        for section in self.__sections:
            section.print()

    def getInputElement(self) -> UIElement:
        for section in self.__sections:
            element = section.getElementByType('input')
            if element is not None:
                return element
        return None

    def listenUserInput(self):
        element = self.getInputElement()
        if element is not None:
            element.listenUserInput()

    def clear(self):
        section: UISection
        for section in self.__sections:
            section.clear()
        self.refresh()
