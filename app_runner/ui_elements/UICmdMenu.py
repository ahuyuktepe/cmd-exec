import math

from app_runner.classes.RecordPaginator import RecordPaginator
from app_runner.enums.UIColor import UIColor
from app_runner.events.EventManager import EventManager
from app_runner.events.FlowEventType import FlowEventType
from app_runner.menu.Command import Command
from app_runner.menu.Menu import Menu
from app_runner.ui_elements.UIElement import UIElement


class UICmdMenu(UIElement):
    __menu: Menu
    __recordPaginator: RecordPaginator

    def __init__(self):
        super().__init__('cmd-menu', 'cmdMenu')
        self.__recordPaginator = None

    # Setter Methods

    def displayCommandsInMenu(self, menu: Menu):
        self.__menu = menu
        self.__setRecordPaginator()
        self.__recordPaginator.setActiveIndex(0)
        self.__printMenuCommands()

    # Getter Methods

    def getActiveCommand(self) -> Command:
        cmd = self.__recordPaginator.getActiveRecord()
        return cmd

    # Utility Methods

    def reset(self, isActive: bool = True):
        if isActive:
            self.__recordPaginator.setActiveIndex(0)
        else:
            self.__recordPaginator.setActiveIndex(-1)
        self.__printMenuCommands()

    # Event Handlers

    def moveUp(self):
        if not self.__recordPaginator.isFirstRecordOnFirstPage():
            self.__recordPaginator.moveToPreviousRecord()
            self.clear()
            self.__printMenuCommands()
            self.refresh()

    def moveDown(self):
        if not self.__recordPaginator.isLastRecordOnLastPage():
            self.__recordPaginator.moveToNextRecord()
            self.clear()
            self.__printMenuCommands()
            self.refresh()

    # Private Methods

    def __setRecordPaginator(self):
        if self.__recordPaginator is not None:
            del self.__recordPaginator
        if self.__menu is not None:
            cmdCount = self.getHeight() - 5
            cmds = self.__menu.getCommandsAsList()
            self.__recordPaginator = RecordPaginator(cmds, cmdCount)

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
            self.refresh()

    def __printCommand(self, y: int, index: int, cmd: Command):
        desc = cmd.getDescription()
        if self.__recordPaginator.getActiveIndex() == index:
            self._printArea.printText(2, y, desc, UIColor.ACTIVE_COMMAND_COLOR)
        else:
            self._printArea.printText(2, y, desc)

    def __getHeight(self) -> int:
        height = self.__recordPaginator.getRecordCountInCurrentPage()
        return height
