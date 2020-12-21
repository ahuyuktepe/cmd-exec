from app_runner.classes.RecordPaginator import RecordPaginator
from app_runner.enums.UIColor import UIColor
from app_runner.events.EventManager import EventManager
from app_runner.events.FlowEventType import FlowEventType
from app_runner.field.Field import Field
from app_runner.form_elements.FormElement import FormUIElement
from app_runner.services.FieldService import FieldService
from app_runner.utils.ListUtil import ListUtil
from app_runner.utils.StrUtil import StrUtil


class MultiChoiceFormElement(FormUIElement):
    __options: list
    __selectedOptions: list
    __printedOptionCount: int
    __maxOptionLineCount: int = 10
    __width: int = 30
    __recordPaginator: RecordPaginator
    __isMultiSelect: bool
    __exit: bool

    def __init__(self, field: Field, isMultiSelect: bool, fieldService: FieldService):
        super().__init__(field, fieldService)
        self.__isMultiSelect = isMultiSelect
        self.__options = field.getOptions()
        self.__selectedOptions = []
        self._value = []
        self.__recordPaginator = RecordPaginator(self.__options, self.__maxOptionLineCount)
        self.__exit = False

    # Utility Methods

    def collectUserInput(self):
        self.display()
        self.__listenEvents()

    def display(self):
        y = 1
        label = self._field.getLabel()
        if self.isSelected():
            label = u'\u00BB' + ' ' + label
        label = StrUtil.getAlignedAndLimitedStr(label, self.getWidth(), 'left')
        self.clear()
        self._printArea.printText(1, y, label)
        # Print Validation Errors
        self.printValidationErrors(y)
        self.__printOptions()
        self.refresh()

    # Event Handlers

    def upKeyPressed(self, data):
        if not self.__recordPaginator.isFirstRecordOnFirstPage():
            self.__recordPaginator.moveToPreviousRecord()
            self.display()

    def downKeyPressed(self, data):
        if not self.__recordPaginator.isLastRecordOnLastPage():
            self.__recordPaginator.moveToNextRecord()
            self.display()

    def enterKeyPressed(self, data):
        self.__setValue()
        self.__recordPaginator.setActiveIndex(-1)
        self.display()
        EventManager.removeListenersByElementId(self.getId())
        EventManager.triggerEvent(FlowEventType.FORM_ELEMENT_VALUE_ENTERED)

    def multiChoiceOptionSelected(self, data):
        selectedOption = self.__recordPaginator.getActiveRecord()
        if not self.__isMultiSelect:
            self.__selectedOptions.clear()
        if not self.__isOptionSelected(selectedOption):
            self.__selectedOptions.append(selectedOption)
        else:
            ListUtil.removeElementByKey(self.__selectedOptions, 'id', selectedOption['id'])
        self.display()

    # Getter Methods

    def getCalculatedHeight(self) -> int:
        return len(self.__options) + 3 + self._fieldValidationErrors.getErrorCount()

    # Private Methods

    def __printOptions(self):
        y = self.getErrorLineCount() + 2
        # Print Previous Page Icon
        if self.__recordPaginator.hasPreviousPage():
            iconStr = StrUtil.getAlignedAndLimitedStr(u' \u25B2 ', self.__width, 'center')
            self._printArea.printText(3, y, iconStr)
        y += 1
        # Print Options
        options = self.__recordPaginator.getRecordsInPage()
        i = 0
        for option in options:
            label = self.__getOptionLabel(option)
            if self.__recordPaginator.getActiveIndex() == i:
                self._printArea.printText(3, y, label, UIColor.ACTIVE_COMMAND_COLOR)
            else:
                self._printArea.printText(3, y, label)
            i += 1
            y += 1
        # Print Next Page Icon
        if self.__recordPaginator.hasNextPage():
            iconStr = StrUtil.getAlignedAndLimitedStr(u' \u25BC ', self.__width, 'center')
            self._printArea.printText(3, y, iconStr)

    def __getOptionLabel(self, option: dict) -> str:
        retStr = '['

        if self.__isOptionSelected(option):
            retStr += '*'
        else:
            retStr += ' '
        retStr += '] ' + StrUtil.getAlignedAndLimitedStr(option['label'], self.__width, 'left')
        return retStr

    def __setValue(self):
        self._value.clear()
        for option in self.__selectedOptions:
            self._value.append(option['id'])

    def __isOptionSelected(self, option: dict):
        return ListUtil.hasElementByKey(self.__selectedOptions, 'id', option['id'])

    def __listenEvents(self):
        pass
