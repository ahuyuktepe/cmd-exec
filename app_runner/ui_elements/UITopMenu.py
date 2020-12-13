import math
from app_runner.classes.RecordPaginator import RecordPaginator
from app_runner.enums.UIColor import UIColor
from app_runner.ui_elements.UIElement import UIElement
from app_runner.utils.StrUtil import StrUtil


class UITopMenu(UIElement):
    __menuNameWidth: int
    __menuCountPerPage: int
    __recordPaginators: list
    __activeIndex: int

    def __init__(self, nameWidth: int):
        super().__init__('top-menu', 'topMenu')
        self.__recordPaginators = []
        self.__menuNameWidth = nameWidth

    def initialize(self):
        self.__menuCountPerPage = math.floor(self.getWidth() / self.__menuNameWidth)

    # Getter Methods

    def getActiveMenu(self):
        record = self.getRecordPaginator().getActiveRecord()
        return record

    def getRecordPaginator(self) -> RecordPaginator:
        obj = self.__recordPaginators[self.__activeIndex]
        return obj.get('recordPaginator')

    # Event Listeners

    def displayMenus(self, data: dict):
        self.clear()
        menus = data.get('menus')
        parentMenuName = data.get('parentMenuName')
        recordPaginator = RecordPaginator(menus, self.__menuCountPerPage)
        recordPaginator.setActiveIndex(0)
        self.__recordPaginators.append({
            'parentMenuName': parentMenuName,
            'recordPaginator': recordPaginator
        })
        self.__activeIndex = len(self.__recordPaginators) - 1
        self.display()
        self.refresh()

    # Utility Methods

    def movePreviousMenus(self):
        if self.__activeIndex > 0:
            del self.__recordPaginators[-1]
            self.__activeIndex -= 1
            self.clear()
            self.display()
            self.refresh()

    def moveLeft(self):
        self.clear()
        self.getRecordPaginator().moveToPreviousRecord()
        self.display()
        self.refresh()

    def moveRight(self):
        self.clear()
        self.getRecordPaginator().moveToNextRecord()
        self.display()
        self.refresh()

    def display(self):
        menuNames: list = self.__getMenuNamesInCurrentPage()
        initialX = 1
        # Print Previous Page Icon If Applicable
        if self.getRecordPaginator().hasPreviousPage():
            self.__printAvailablePageIcon(u'\u00AB', 5, initialX)
            initialX += 5
        # Print Commands
        for i in range(0, len(menuNames)):
            name = menuNames[i]
            x = (self.__menuNameWidth * i) + initialX
            self.__printMenuName(name, x, i)
        # Print Next Page Icon If Applicable
        if self.getRecordPaginator().hasNextPage():
            self.__printAvailablePageIcon(u'\u00BB', 5, self.getWidth() - 6)
        self.__printPreviousMenusIcon()

    # Private Methods

    def __getMenuNamesInCurrentPage(self) -> list:
        menus = self.getRecordPaginator().getRecordsInPage()
        menuNames = []
        for menu in menus:
            menuNames.append(menu.getName())
        return menuNames

    def __printAvailablePageIcon(self, text: str, width: int, x: int):
        text = StrUtil.getAlignedAndLimitedStr(text, width, 'center')
        self._printArea.printText(x, 0, text)

    def __printPreviousMenusIcon(self):
        if self.__activeIndex > 0:
            obj = self.__recordPaginators[self.__activeIndex]
            self._printArea.printText(0, 1,  u'\u00AB ' + obj.get('parentMenuName') + ' (r)')

    def __printMenuName(self, name: str, x: int, index: int):
        name = StrUtil.getAlignedAndLimitedStr(name, self.__menuNameWidth, 'center')
        if index == self.getRecordPaginator().getActiveIndex():
            self._printArea.printText(x, 0, name, UIColor.ACTIVE_COMMAND_COLOR)
        else:
            self._printArea.printText(x, 0,  name)
