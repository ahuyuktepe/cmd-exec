import curses
import math
from xml.etree.ElementTree import Element
from app_runner.app.context.AppContext import AppContext
from app_runner.events.EventManager import EventManager
from app_runner.events.UIEventType import UIEventType
from app_runner.menu.Command import Command
from app_runner.menu.Menu import Menu
from app_runner.ui.terminal.classes.RecordPaginator import RecordPaginator
from app_runner.ui.terminal.element.UIElement import UIElement
from app_runner.ui.terminal.enums.UIColor import UIColor
from app_runner.ui.utils.XmlElementUtil import XmlElementUtil


class MenuElement(UIElement):
    __menu: Menu
    __recordPaginator: RecordPaginator

    def __init__(self, id: str, appContext: AppContext):
        super().__init__(id, 'menu', appContext)
        self.__recordPaginator = None
        self.__menu = None

    # Setter Methods

    def setAttributes(self, element: Element):
        super().setAttributes(element)
        parent = self.getParent()
        # Set Dimensions
        width = XmlElementUtil.getAttrValueAsInt(element, 'width', 40)
        height = XmlElementUtil.getAttrValueAsInt(element, 'height', 10)
        self.setDimensions(width, height)
        # Set Window
        defaultX = math.floor((parent.getWidth() - self.getWidth()) / 2)
        defaultY = math.floor((parent.getHeight() - self.getHeight()) / 2)
        x = XmlElementUtil.getAttrValueAsInt(element, 'x', defaultX)
        y = XmlElementUtil.getAttrValueAsInt(element, 'y', defaultY)
        self.setLocation(x, y)

    def setListeners(self):
        EventManager.listenEvent(UIEventType.UP_KEY_PRESSED, self)
        EventManager.listenEvent(UIEventType.DOWN_KEY_PRESSED, self)
        EventManager.listenEvent(UIEventType.ENTER_KEY_PRESSED, self)
        EventManager.listenEvent(UIEventType.DISPLAY_COMMANDS, self)

    # Event Handler

    def enterKeyPressed(self, data: dict):
        cmd = self.__recordPaginator.getActiveRecord()
        EventManager.triggerEvent(UIEventType.COMMAND_SELECTED, {
            'command': cmd
        })

    def displayCommands(self, data: dict):
        self.__menu = data.get('menu')
        self.__setRecordPaginator(self.__menu)
        self.__printMenuCommands()
        self.refresh()

    def upKeyPressed(self, data: dict):
        if not self.__recordPaginator.isFirstRecordOnFirstPage():
            self.__recordPaginator.moveToPreviousRecord()
            self.clear()
            self.__printMenuCommands()
            self.refresh()

    def downKeyPressed(self, data: dict):
        if not self.__recordPaginator.isLastRecordOnLastPage():
            self.__recordPaginator.moveToNextRecord()
            self.clear()
            self.__printMenuCommands()
            self.refresh()

    # Private Methods

    def __printMenuCommands(self):
        if self.__menu is not None:
            self.clear()
            self.displayBorder()
            self._window.addstr(1, 1, ("{0:^" + str(self.getWidth()-2) + "}").format(self.__menu.getName()))
            self._window.hline(2, 1, curses.ACS_HLINE, (self.getWidth()-2))
            cmds: list = self.__recordPaginator.getRecordsInPage()
            startY = 3
            height = self.__getHeight()
            for i in range(0, height):
                self.__printCommand((i + startY), i, cmds[i])
            if self.__recordPaginator.hasNextPage():
                self._window.addstr(height+3, math.floor((self.getWidth()-4)/2), u' \u25BC  ')
            if self.__recordPaginator.hasPreviousPage():
                self._window.addstr(2, math.floor((self.getWidth()-4)/2), u' \u25B2 ')

    def __getHeight(self) -> int:
        height = self.__recordPaginator.getRecordCountInCurrentPage()
        return height

    def __printCommand(self, y: int, index: int, cmd: Command):
        desc = cmd.getDescription()
        if self.__recordPaginator.getActiveIndex() == index:
            self._window.addstr(y, 2, desc, curses.color_pair(UIColor.ACTIVE_COMMAND_COLOR))
        else:
            self._window.addstr(y, 2, desc)

    def __setRecordPaginator(self, menu: Menu):
        if self.__recordPaginator is not None:
            del self.__recordPaginator
        if menu is not None:
            cmdCount = self.getHeight() - 4
            cmds = list(menu.getCommands().values())
            self.__recordPaginator = RecordPaginator(cmds, cmdCount)
