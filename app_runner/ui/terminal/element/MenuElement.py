from app_runner.menu.Menu import Menu
from app_runner.ui.terminal.element.UIElement import UIElement


class MenuElement(UIElement):
    __menus: list
    __nid: str

    def __init__(self, id: str, nid: str):
        super().__init__(id, 'menu')
        self.__menus = []
        self.__nid = nid

    def addMenu(self, menu: Menu):
        self.__menus.append(menu)

    def print(self, data: dict = {}):
        self.refresh()
