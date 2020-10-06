import curses

from app_runner.app.context.AppContext import AppContext
from app_runner.events.EventManager import EventManager
from app_runner.events.UIEventType import UIEventType
from app_runner.ui.terminal.element.UIElement import UIElement
from app_runner.ui.terminal.element.UISection import UISection


class UIView(UIElement):
    __sections: list

    def __init__(self, id: str, appContext: AppContext):
        super().__init__(id, 'view', appContext)
        self.__sections = []

    # Setter Methods

    def addSection(self, section: UISection):
        if section is not None:
            self.__sections.append(section)

    # Utility Methods

    def initialize(self):
        self._window = curses.initscr()
        curses.cbreak()
        curses.noecho()
        self._window.nodelay(True)
        self._x = 0
        self._y = 0
        self._height, self._width = self._window.getmaxyx()

    def print(self):
        section: UISection
        for section in self.__sections:
            section.print()
            section.setup()
        self.setup()
        EventManager.triggerEvent(UIEventType.VIEW_LOADED)
