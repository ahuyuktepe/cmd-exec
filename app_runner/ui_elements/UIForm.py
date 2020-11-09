from app_runner.classes.FormManager import FormManager
from app_runner.events.EventManager import EventManager
from app_runner.events.UIEventType import UIEventType
from app_runner.field.Field import Field
from app_runner.form_elements.FormUIElement import FormUIElement
from app_runner.ui_elements.UIElement import UIElement
from app_runner.form_elements.TextElement import TextElement
from app_runner.utils.StrUtil import StrUtil
from app_runner.utils.UIPrintAreaUtil import UIPrintAreaUtil


class UIForm(UIElement):
    __title: str
    __fields: list
    __formManager: FormManager
    __values: dict
    # Static Variables
    _pageInfoWidth = 15

    def __init__(self, id: str, title: str, fields: list):
        super().__init__(id, 'form')
        self.__fields = fields
        self.__title = title
        self.__formManager = FormManager()
        self.__values = {}

    # Setter Methods

    def setListeners(self):
        EventManager.listenEvent(UIEventType.COLLECT_FIELD_VALUES, self)

    # Utility Methods

    def display(self):
        self.__formManager.reset()
        self.__buildFormElements()
        self.__printForm()

    # Event Handlers

    def collectFieldValues(self, data: dict):
        self.__setFieldValuesByUserInput()
        EventManager.triggerEvent(UIEventType.FIELD_VALUES_COLLECTED, {
            'values': self.__values
        })

    # Private Methods

    def __printForm(self):
        self.clear()
        self.__formManager.updateSelection()
        self.__printElementsInCurrentPage()
        self.__printPageInfo()
        self.__printFormTitle()

    def __printFormTitle(self):
        titleWidth = self.getWidth() - self._pageInfoWidth
        formTitle = StrUtil.getAlignedAndLimitedStr(self.__title, titleWidth, 'center')
        self._printArea.printText(1, 1, formTitle)

    def __printPageInfo(self):
        pageCount = self.__formManager.getPageCount()
        currentPage = self.__formManager.getPage() + 1
        pageInfo = 'Page ' + str(currentPage) + '/' + str(pageCount)
        if self.__formManager.hasPreviousPage():
            pageInfo = u'\u00AB' + ' ' + pageInfo
        else:
            pageInfo = '  ' + pageInfo
        if self.__formManager.hasNextPage():
            pageInfo = pageInfo + ' ' + u'\u00BB'
        else:
            pageInfo += '  '
        pageInfo = StrUtil.getAlignedAndLimitedStr(pageInfo, self._pageInfoWidth, 'right')
        x = self.getWidth() - self._pageInfoWidth - 2
        self._printArea.printText(x, 1, pageInfo)

    def __printElementsInCurrentPage(self):
        elementsInCurrentPage = self.__formManager.getElementsInCurrentPage()
        for element in elementsInCurrentPage:
            element.display()
            element.setListeners()

    def __setFieldValuesByUserInput(self):
        userInput: dict = self.__fetchUserInput()
        while userInput['action'] != 'submit':
            activeElement = userInput['active_element']
            self.__values[activeElement.getId()] = activeElement.getUserInput()
            userInput: dict = self.__fetchUserInput()

    def __fetchUserInput(self):
        userInput: dict = {}
        exitWhile = False
        while not exitWhile:
            selection = self._printArea.getUserInput()
            if selection == 'w' and not self.__formManager.isFirstIndexOnFirstPage():
                self.__formManager.decreaseActiveIndex()
                self.__printForm()
            elif selection == 's' and not self.__formManager.isLastIndexOnLastPage():
                self.__formManager.increaseActiveIndex()
                self.__printForm()
            elif selection == 'a' and self.__formManager.hasPreviousPage():
                self.__formManager.movePrePage()
                self.__printForm()
            elif selection == 'd' and self.__formManager.hasNextPage():
                self.__formManager.moveNextPage()
                self.__printForm()
            elif selection == 'e':
                userInput['active_element'] = self.__formManager.getActiveField()
                userInput['action'] = 'field-selection'
                exitWhile = True
            elif selection == 'q':
                userInput['action'] = 'submit'
                exitWhile = True
        return userInput

    def __buildFormElements(self):
        availableHeight = self.getHeight() - 3
        initialY = 2
        y = initialY
        page = 0
        element: FormUIElement = None
        for field in self.__fields:
            if y >= availableHeight:
                y = initialY
                page += 1
            if field.isText():
                element = self.__buildTextElement(field, y)
            if element is not None:
                self.__formManager.addElement(page, element)
                y += element.getHeight()

    def __buildTextElement(self, field: Field, y: int) -> TextElement:
        element = TextElement(field)
        # Set Print Area
        # TODO: Height should be dynamic depending on validation message or border.
        width = self.getWidth() - 2
        height = element.getCalculatedHeight()
        printArea = UIPrintAreaUtil.buildDerivedPrintArea(1, y, width, height, self._printArea)
        element.setPrintArea(printArea)
        return element
