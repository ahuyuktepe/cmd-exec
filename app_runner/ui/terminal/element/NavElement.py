from app_runner.menu.Menu import Menu
from app_runner.ui.terminal.element.UIElement import UIElement


class NavElement(UIElement):
    __menus: list
    __mid: str

    def __init__(self, id: str, mid: str):
        super().__init__(id, 'nav')
        self.__menus = ['Development', 'QA', 'Deployment', 'Production']
        self.__mid = mid

    def addMenu(self, menu: Menu):
        self.__menus.append(menu)

    def print(self, data: dict = {}):
        menu: Menu
        x = 2
        for name in self.__menus:
            self._window.addstr(1, x, name)
            x += len(name) + 1
            self._window.addstr(1, x, ' | ')
            x += 3
