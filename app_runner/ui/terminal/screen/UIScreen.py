import curses
from app_runner.ui.terminal.element.UIElement import UIElement
from app_runner.ui.terminal.screen.UISection import UISection


class UIScreen(UIElement):
    _window: object
    _sections: dict = {}
    _title: str

    def __init__(self, id: str, title: str):
        super().__init__(id, 'screen')
        self._title = title

    def initialize(self):
        self._window = curses.initscr()
        self._x = 0
        self._y = 0
        self._height, self._width = self._window.getmaxyx()
        self.__setColors()

    def __setColors(self):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

    def addSection(self, section: UISection):
        if section is not None:
            self._sections[section.getId()] = section

    def getSection(self, sid: str) -> UISection:
        return self._sections.get(sid)

    def print(self):
        section: UISection
        for sid, section in self._sections.items():
            section.print()

    def getTitle(self) -> str:
        return self._title
