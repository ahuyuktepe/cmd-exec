import curses
import math
from xml.etree.ElementTree import Element
from app_runner.events.EventManager import EventManager
from app_runner.events.UIEventType import UIEventType
from app_runner.menu.Command import Command
from app_runner.menu.Menu import Menu
from app_runner.classes.RecordPaginator import RecordPaginator
from app_runner.ui_elements.UIElement import UIElement
from app_runner.enums.UIColor import UIColor


class UIMenu(UIElement):
    __menu: Menu
    __recordPaginator: RecordPaginator

    def __init__(self, id: str):
        super().__init__(id, 'menu')
        self.__recordPaginator = None
        self.__menu = None

    # Setter Methods

    def setAttributes(self, element: Element):
        super().setAttributes(element)

    def setListeners(self):
        EventManager.listenEvent(UIEventType.UP_KEY_PRESSED, self)
        EventManager.listenEvent(UIEventType.DOWN_KEY_PRESSED, self)
        EventManager.listenEvent(UIEventType.ENTER_KEY_PRESSED, self)
        EventManager.listenEvent(UIEventType.DISPLAY_COMMANDS, self)

    # Event Handlers

    def enterKeyPressed(self, data: dict):
        cmd = self.__recordPaginator.getActiveRecord()
        EventManager.triggerEvent(UIEventType.COMMAND_SELECTED, {
            'command': cmd
        })

    def displayCommands(self, data: dict):
        self.__menu = data.get('menu')
        self.__setRecordPaginator(self.__menu)
        self.__printMenuCommands()
        self._printArea.addBorder()
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
            self._printArea.printText(1, 1, ("{0:^" + str(self.getWidth()-2) + "}").format(self.__menu.getName()))
            self._printArea.printLine(1, 2, self.getWidth() - 2)
            cmds: list = self.__recordPaginator.getRecordsInPage()
            startY = 3
            height = self.__getHeight()
            for i in range(0, height):
                self.__printCommand((i + startY), i, cmds[i])
            if self.__recordPaginator.hasNextPage():
                self._printArea.printText(math.floor((self.getWidth() - 4) / 2), height + 3, u' \u25BC  ')
            if self.__recordPaginator.hasPreviousPage():
                self._printArea.printText(math.floor((self.getWidth() - 4) / 2), 2, u' \u25B2 ')
            self._printArea.addBorder()

    def __getHeight(self) -> int:
        height = self.__recordPaginator.getRecordCountInCurrentPage()
        return height

    def __printCommand(self, y: int, index: int, cmd: Command):
        desc = cmd.getDescription()
        if self.__recordPaginator.getActiveIndex() == index:
            self._printArea.printText(2, y, desc, UIColor.ACTIVE_COMMAND_COLOR)
        else:
            self._printArea.printText(2, y, desc)

    def __setRecordPaginator(self, menu: Menu):
        if self.__recordPaginator is not None:
            del self.__recordPaginator
        if menu is not None:
            cmdCount = self.getHeight() - 5
            cmds = list(menu.getCommands().values())
            self.__recordPaginator = RecordPaginator(cmds, cmdCount)
