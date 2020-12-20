from app_runner.classes.FormElementBuilder import FormElementBuilder
from app_runner.classes.FormManager import FormManager
from app_runner.errors.FieldValidationErrors import FieldValidationErrors
from app_runner.events.EventManager import EventManager
from app_runner.events.UIEventType import UIEventType
from app_runner.menu.Command import Command
from app_runner.services.FieldService import FieldService
from app_runner.ui_elements.UIElement import UIElement
from app_runner.utils.StrUtil import StrUtil


class UIForm(UIElement):
    __title: str
    __cmd: Command
    __formManager: FormManager
    __fieldService: FieldService
    __values: dict
    __userInput: dict
    __isFormSubmitted: bool
    # Static Variables
    _pageInfoWidth = 15

    def __init__(self, id: str, title: str, cmd: Command, fieldService: FieldService):
        super().__init__(id, 'form')
        self.__cmd = cmd
        self.__title = title
        self.__formManager = FormManager()
        self.__fieldService = fieldService
        self.__values = {}
        self.__userInput = {}
        self.__isFormSubmitted = False

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
        isValid = False
        formElementBuilder = FormElementBuilder(self.__formManager, self.getPrintArea(), self.__fieldService, self.__cmd.getModuleId())
        while not isValid:
            if not self.__formManager.areValuesValid():
                formElementBuilder.refreshElements()
                self.__printForm()
                isValid = False
            else:
                isValid = True
        EventManager.triggerEvent(UIEventType.FIELD_VALUES_COLLECTED, {
            'values': self.__values
        })

    def upKeyPressed(self):
        if not self.__formManager.isFirstIndexOnFirstPage():
            self.__formManager.decreaseActiveIndex()
            self.__printForm()

    def downKeyPressed(self):
        if not self.__formManager.isLastIndexOnLastPage():
            self.__formManager.increaseActiveIndex()
            self.__printForm()

    def leftKeyPressed(self):
        if self.__formManager.hasPreviousPage():
            self.__formManager.movePrePage()
            self.__printForm()

    def rightKeyPressed(self):
        if self.__formManager.hasNextPage():
            self.__formManager.moveNextPage()
            self.__printForm()

    def enterKeyPressed(self):
        activeElement = self.__formManager.getActiveField()
        self.__values[activeElement.getId()] = activeElement.getUserInput()

    def quitKeyPressed(self):
        self.__formManager.validateFormValues()

    # Private Methods

    def __printForm(self):
        self.clear()
        self.__formManager.updateSelection()
        self.__printHeader()
        self.__printElementsInCurrentPage()

    def __printHeader(self):
        # Print Title
        titleWidth = self.getWidth() - self._pageInfoWidth
        formTitle = StrUtil.getAlignedAndLimitedStr(self.__title, titleWidth, 'center')
        self._printArea.printText(1, 0, formTitle)
        # Print Page Information
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
        self._printArea.printText(x, 0, pageInfo)

    def __printElementsInCurrentPage(self):
        elementsInCurrentPage = self.__formManager.getElementsInCurrentPage()
        for element in elementsInCurrentPage:
            element.display()
            element.setListeners()

    def __buildFormElements(self):
        formElementBuilder = FormElementBuilder(self.__formManager, self.getPrintArea(), self.__fieldService, self.__cmd.getModuleId())
        formElementBuilder.reset()
        for field in self.__cmd.getFieldsAsList():
            formElementBuilder.buildElementsAndAdd(field)
