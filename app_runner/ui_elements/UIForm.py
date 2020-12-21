import math

from app_runner.classes.FormElementBuilder import FormElementBuilder
from app_runner.classes.FormFieldValueGetter import FormFieldValueGetter
from app_runner.classes.FormManager import FormManager
from app_runner.events.EventManager import EventManager
from app_runner.events.FlowEventType import FlowEventType
from app_runner.menu.Command import Command
from app_runner.services.FieldService import FieldService
from app_runner.ui_elements.UIElement import UIElement
from app_runner.utils.StrUtil import StrUtil


class UIForm(UIElement):
    __title: str
    __formManager: FormManager
    __fieldService: FieldService
    __values: dict
    __userInput: dict
    __isFormSubmitted: bool
    __cmd: Command
    # Static Variables
    _pageInfoWidth = 15

    def __init__(self, id: str, fieldService: FieldService):
        super().__init__(id, 'form')
        self.__formManager = FormManager()
        self.__fieldService = fieldService
        self.__values = {}
        self.__userInput = {}
        self.__isFormSubmitted = False

    # Getter Methods

    def getCommandArguments(self, cmd: Command) -> dict:
        self.__cmd = cmd
        formElementBuilder: FormElementBuilder = self.__displayFields(cmd)
        isValid = False
        while not isValid:
            if not self.__formManager.areValuesValid():
                formElementBuilder.refreshElements()
                self.__printForm()
                isValid = False
            else:
                isValid = True
        return self.__values

    # Utility Methods

    def listenEvents(self):
        EventManager.listenEvent(FlowEventType.FORM_ELEMENT_VALUE_ENTERED, self)
        EventManager.listenEvent(FlowEventType.SUBMIT_FORM, self)

    # Event Handlers

    def formElementValueEntered(self, data):
        self.listenEvents()

    def upKeyPressed(self, data):
        if not self.__formManager.isFirstIndexOnFirstPage():
            self.__formManager.decreaseActiveIndex()
            self.__printForm()

    def downKeyPressed(self, data):
        if not self.__formManager.isLastIndexOnLastPage():
            self.__formManager.increaseActiveIndex()
            self.__printForm()

    def leftKeyPressed(self, data):
        if self.__formManager.hasPreviousPage():
            self.__formManager.movePrePage()
            self.__printForm()

    def rightKeyPressed(self, data):
        if self.__formManager.hasNextPage():
            self.__formManager.moveNextPage()
            self.__printForm()

    def enterKeyPressed(self, data):
        EventManager.removeListenersByElementId(self.getId(), [
            FlowEventType.FORM_ELEMENT_VALUE_ENTERED
        ])
        activeElement = self.__formManager.getActiveField()
        activeElement.collectUserInput()

    def submitForm(self, data):
        self.__formManager.validateFormValues()

    # Private Methods

    def __displayFields(self, cmd: Command) -> FormElementBuilder:
        self.__formManager.reset()
        # Build Elements
        formElementBuilder = FormElementBuilder(self.__formManager, self.getPrintArea(), self.__fieldService)
        formElementBuilder.reset()
        for field in cmd.getFieldsAsList():
            formElementBuilder.buildElementsAndAdd(field)
        self.__printForm()
        return formElementBuilder

    def __printForm(self):
        self.clear()
        self.__printButtons()
        self.__formManager.updateSelection()
        # self.__printHeader()
        self.__printElementsInCurrentPage()

    def __printHeader(self):
        # Print Title
        titleWidth = self.getWidth() - self._pageInfoWidth
        cmdDesc = self.__cmd.getDescription()
        formTitle = StrUtil.getAlignedAndLimitedStr(cmdDesc, titleWidth, 'center')
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
            element.listenEvents()

    def __printButtons(self):
        width = self.getWidth()
        x = math.floor((width - 24) / 2)
        y = self.getHeight() - 1
        text = StrUtil.getAlignedAndLimitedStr('[ Submit ]', 11, 'center')
        self._printArea.printText(x, y, text)
        text = StrUtil.getAlignedAndLimitedStr('[ Cancel ]', 11, 'center')
        x += 13
        self._printArea.printText(x, y, text)
        self.refresh()
