import curses
import math
from xml.etree.ElementTree import Element
from app_runner.events.EventManager import EventManager
from app_runner.events.UIEventType import UIEventType
from app_runner.ui_elements.UIElement import UIElement
from app_runner.classes.RecordPaginator import RecordPaginator
from app_runner.enums.UIColor import UIColor
from app_runner.utils.XmlElementUtil import XmlElementUtil
from app_runner.utils.StrUtil import StrUtil


class UINavigation(UIElement):
    __menus: list
    __recordPaginator: RecordPaginator
    __recordPaginators: list
    __activePaginator: int
    __menuNameWidth: int
    __menuCountPerPage: int

    def __init__(self, id: str):
        super().__init__(id, 'nav')
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
        super().setAttributes(element)
        self.__menuNameWidth = XmlElementUtil.getAttrValueAsInt(element, 'nameWidth', 20)
        self.__menuCountPerPage = math.floor(self.getWidth() / self.__menuNameWidth)

    def setRecordPaginator(self):
        self.__recordPaginator = RecordPaginator(self.__menus, self.__menuCountPerPage)
        self.__recordPaginators.append(self.__recordPaginator)
        self.__activePaginator = len(self.__recordPaginators) - 1

    def setMenus(self, menus: list):
        self.__menus = menus
        self.setRecordPaginator()

    # Event Listeners

    def displayPreviousMenus(self, data: dict):
        if self.__activePaginator > 0:
            del self.__recordPaginators[self.__activePaginator]
            self.__activePaginator -= 1
            self.__recordPaginator = self.__recordPaginators[self.__activePaginator]
            self.clear()
            self.display()
            self.refresh()
            self.__notifyMenuElementToPrintCommands()

    def displayMenus(self, data: dict = {}):
        menus = data.get('menus')
        if menus is not None:
            self.setMenus(menus)
        self.clear()
        self.display()
        self.refresh()
        self.__notifyMenuElementToPrintCommands()

    def viewLoaded(self, data: dict):
        self.__notifyMenuElementToPrintCommands()

    def leftKeyPressed(self, data: dict):
        if not self.__recordPaginator.isFirstRecordOnFirstPage():
            self.__recordPaginator.moveToPreviousRecord()
            self.clear()
            self.display()
            self.refresh()
            self.__notifyMenuElementToPrintCommands()

    def rightKeyPressed(self, data: dict):
        if not self.__recordPaginator.isLastRecordOnLastPage():
            self.__recordPaginator.moveToNextRecord()
            self.clear()
            self.display()
            self.refresh()
            self.__notifyMenuElementToPrintCommands()

    # Utility Methods

    def display(self):
        menuNames: list = self.__getMenuNamesInCurrentPage()
        initialX = 1
        # Print Previous Page Icon If Applicable
        if self.__recordPaginator.hasPreviousPage():
            self.__printAvailablePageIcon(u'\u00AB', 5, initialX)
            initialX += 5
        # Print Commands
        for i in range(0, len(menuNames)):
            name = menuNames[i]
            x = (self.__menuNameWidth * i) + initialX
            self.__printMenuName(name, x, i)
        # Print Next Page Icon If Applicable
        if self.__recordPaginator.hasNextPage():
            self.__printAvailablePageIcon(u'\u00BB', 5, self.getWidth() - 6)
        self.__printPreviousMenusIcon()

    # Private Methods

    def __printPreviousMenusIcon(self):
        if self.hasPreviousMenus():
            self._printArea.printText(0, 1,  u'\u00AB Previous Menus (r)')

    def __printAvailablePageIcon(self, text: str, width: int, x: int):
        text = StrUtil.getAlignedAndLimitedStr(text, width, 'center')
        self._printArea.printText(x, 0, text)

    def __getMenuNamesInCurrentPage(self) -> list:
        menus = self.__recordPaginator.getRecordsInPage()
        menuNames = []
        for menu in menus:
            menuNames.append(menu.getName())
        return menuNames

    def __printMenuName(self, name: str, x: int, index: int):
        name = StrUtil.getAlignedAndLimitedStr(name, self.__menuNameWidth, 'center')
        if index == self.__recordPaginator.getActiveIndex():
            self._printArea.printText(x, 0, name, UIColor.ACTIVE_COMMAND_COLOR)
        else:
            self._printArea.printText(x, 0,  name)

    def __notifyMenuElementToPrintCommands(self):
        EventManager.triggerEvent(UIEventType.DISPLAY_COMMANDS, {
            'menu': self.__recordPaginator.getActiveRecord()
        })
