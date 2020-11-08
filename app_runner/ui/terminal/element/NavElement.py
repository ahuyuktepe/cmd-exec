import curses
import math
from xml.etree.ElementTree import Element
from app_runner.app.context.AppContext import AppContext
from app_runner.events.EventManager import EventManager
from app_runner.events.UIEventType import UIEventType
from app_runner.services.MenuService import MenuService
from app_runner.ui.terminal.classes.RecordPaginator import RecordPaginator
from app_runner.ui.terminal.element.UIElement import UIElement
from app_runner.ui.terminal.enums.UIColor import UIColor
from app_runner.ui.utils.XmlElementUtil import XmlElementUtil
from app_runner.utils.StrUtil import StrUtil


class NavElement(UIElement):
    __menuService: MenuService
    __recordPaginator: RecordPaginator
    __recordPaginators: list
    __activePaginator: int
    __menuNameWidth: int
    __menuCountPerPage: int

    def __init__(self, id: str, appContext: AppContext):
        super().__init__(id, 'nav', appContext)
        self.__menuService = appContext.getService('menuService')
        self.__recordPaginator = 0
        self.__recordPaginators = []

    # Gettter Methods

    def hasPreviousMenus(self) -> bool:
        return len(self.__recordPaginators) > 1

    # Setter Methods

    def setListeners(self):
        EventManager.listenEvent(UIEventType.LEFT_KEY_PRESSED, self)
        EventManager.listenEvent(UIEventType.RIGHT_KEY_PRESSED, self)
        EventManager.listenEvent(UIEventType.VIEW_LOADED, self)
        EventManager.listenEvent(UIEventType.DISPLAY_MENUS, self)
        EventManager.listenEvent(UIEventType.DISPLAY_PREVIOUS_MENUS, self)

    def setAttributes(self, element: Element):
        parent = self.getParent()
        self.setDimensions(parent.getWidth(), 3)
        self.setLocation(1, 1)
        super().setAttributes(element)
        self.__menuNameWidth = XmlElementUtil.getAttrValueAsInt(element, 'nameWidth', 20)
        self.__menuCountPerPage = math.floor(self.getWidth() / self.__menuNameWidth)
        mids = XmlElementUtil.getAttrValueAsStr(element, 'menus', 'main').split(',')
        self.setRecordPaginator(mids)

    def setRecordPaginator(self, mids: list):
        menus = self.__menuService.buildMenus(mids)
        self.__recordPaginator = RecordPaginator(menus, self.__menuCountPerPage)
        self.__recordPaginators.append(self.__recordPaginator)
        self.__activePaginator = len(self.__recordPaginators) - 1

    # Event Listeners

    def displayPreviousMenus(self, data: dict):
        if self.__activePaginator > 0:
            del self.__recordPaginators[self.__activePaginator]
            self.__activePaginator -= 1
            self.__recordPaginator = self.__recordPaginators[self.__activePaginator]
            self.clear()
            self.print()
            self.refresh()
            self.__notifyMenuElementToPrintCommands()

    def displayMenus(self, data: dict):
        mids = data.get('mids')
        self.setRecordPaginator(mids)
        self.clear()
        self.print()
        self.refresh()
        self.__notifyMenuElementToPrintCommands()

    def viewLoaded(self, data: dict):
        self.__notifyMenuElementToPrintCommands()

    def leftKeyPressed(self, data: dict):
        if not self.__recordPaginator.isFirstRecordOnFirstPage():
            self.__recordPaginator.moveToPreviousRecord()
            self.clear()
            self.print()
            self.refresh()
            self.__notifyMenuElementToPrintCommands()

    def rightKeyPressed(self, data: dict):
        if not self.__recordPaginator.isLastRecordOnLastPage():
            self.__recordPaginator.moveToNextRecord()
            self.clear()
            self.print()
            self.refresh()
            self.__notifyMenuElementToPrintCommands()

    # Utility Methods

    def clear(self):
        parent = self.getParent()
        if parent.hasBorder():
            text = ' ' * (self.getWidth() - 2)
        else:
            text = ' ' * self.getWidth()
        self._window.addstr(1, 1, text)
        self._window.addstr(3, 1, text)

    def print(self):
        menuNames: list = self.__getMenuNamesInCurrentPage()
        initialX = 1
        if self.__recordPaginator.hasPreviousPage():
            self.__printAvailablePageIcon(u'\u00AB', 5, initialX)
            initialX += 5
        for i in range(0, len(menuNames)):
            name = menuNames[i]
            x = (self.__menuNameWidth * i) + initialX
            self.__printMenuName(name, x, i)
        if self.__recordPaginator.hasNextPage():
            self.__printAvailablePageIcon(u'\u00BB', 5, self.getWidth()-6)
        self.__printPreviousMenusIcon()

    # Private Methods

    def __printPreviousMenusIcon(self):
        if self.hasPreviousMenus():
            self._window.addstr(3, 1, u'\u00AB Previous Menus (r)')

    def __printAvailablePageIcon(self, text: str, width: int, x: int):
        text = StrUtil.getAlignedAndLimitedStr(text, width, 'center')
        self._window.addstr(1, x, text)

    def __getMenuNamesInCurrentPage(self) -> list:
        menus = self.__recordPaginator.getRecordsInPage()
        menuNames = []
        for menu in menus:
            menuNames.append(menu.getName())
        return menuNames

    def __printMenuName(self, name: str, x: int, index: int):
        name = StrUtil.getAlignedAndLimitedStr(name, self.__menuNameWidth, 'center')
        if index == self.__recordPaginator.getActiveIndex():
            self._window.addstr(1, x, name, curses.color_pair(UIColor.ACTIVE_MENU_COLOR))
        else:
            self._window.addstr(1, x, name)

    def __notifyMenuElementToPrintCommands(self):
        EventManager.triggerEvent(UIEventType.DISPLAY_COMMANDS, {
            'menu': self.__recordPaginator.getActiveRecord()
        })
