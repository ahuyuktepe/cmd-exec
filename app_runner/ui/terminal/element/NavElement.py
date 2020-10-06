import curses
from xml.etree.ElementTree import Element

from app_runner.app.context.AppContext import AppContext
from app_runner.events.EventManager import EventManager
from app_runner.events.UIEventType import UIEventType
from app_runner.services.MenuService import MenuService
from app_runner.ui.terminal.element.UIElement import UIElement
from app_runner.ui.terminal.enums.UIColor import UIColor
from app_runner.ui.terminal.utils.XmlElementUtil import XmlElementUtil
from app_runner.utils.StrUtil import StrUtil


class NavElement(UIElement):
    __menus: list
    __activeMenuIndex: int
    __nameWidth: int
    __menuService: MenuService
    __nameWidth = 20

    def __init__(self, id: str, appContext: AppContext):
        super().__init__(id, 'nav', appContext)
        self.__menus = []
        self.__activeMenuIndex = 0
        self.__menuService = appContext.getService('menuService')

    # Getter Methods

    def hasMenus(self) -> bool:
        return self.__menus is not None and len(self.__menus) > 0

    # Setter Methods

    def setListeners(self):
        EventManager.listenEvent(UIEventType.DISPLAY_MENUS, self)
        EventManager.listenEvent(UIEventType.LEFT_KEY_PRESSED, self)
        EventManager.listenEvent(UIEventType.RIGHT_KEY_PRESSED, self)

    def setAttributes(self, element: Element):
        parent = self.getParent()
        self.setDimensions(parent.getWidth(), 1)
        self.setLocation(1, 1)
        super().setAttributes(element)
        # Set Default Menus
        mids = XmlElementUtil.getAttrValueAsStr(element, 'menus', 'main').split(',')
        self.__menus = self.__menuService.buildMenus(mids)

    # Event Listeners

    def displayMenus(self, data: dict):
        print('displayMenus')

    def leftKeyPressed(self, data: dict):
        self.__decreaseActiveMenuIndex()
        self.print()

    def rightKeyPressed(self, data: dict):
        self.__increaseActiveMenuIndex()
        self.print()

    # Utility Methods

    def print(self, data: dict = {}):
        if self.hasMenus():
            for i in range(0, len(self.__menus)):
                self.printMenuName(i)
            self.refresh()

    # Private Methods

    def printMenuName(self, index: int):
        menu = self.__menus[index]
        name = menu.getName()
        x = 2
        if index > 0:
            x = x + (self.__nameWidth * index)
        if self.__hasEnoughSpaceForMenuName(x):
            name = StrUtil.getAlignedAndLimitedStr(name, self.__nameWidth, 'center')
            if self.__activeMenuIndex == index:
                self._window.addstr(1, x, name, curses.color_pair(UIColor.ACTIVE_MENU_COLOR))
            else:
                self._window.addstr(1, x, name)

    def __hasEnoughSpaceForMenuName(self, x: int) -> bool:
        nextSpace = x + self.__nameWidth
        return nextSpace < self.getWidth()

    def __decreaseActiveMenuIndex(self):
        if self.__activeMenuIndex == 0:
            self.__activeMenuIndex = len(self.__menus)-1
        else:
            self.__activeMenuIndex -= 1

    def __increaseActiveMenuIndex(self):
        if self.__activeMenuIndex == len(self.__menus)-1:
            self.__activeMenuIndex = 0
        else:
            self.__activeMenuIndex += 1