from app_runner.classes.RecordPaginator import RecordPaginator
from app_runner.enums.UIColor import UIColor
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
    __maxErrorLineCount: int = 4
    __width: int = 30
    __recordPaginator: RecordPaginator
    __isMultiSelect: bool

    def __init__(self, field: Field, isMultiSelect: bool, mid: str, fieldService: FieldService):
        super().__init__(field, mid, fieldService)
        self.__isMultiSelect = isMultiSelect
        self.__options = field.getOptions()
        self.__selectedOptions = []
        self._value = []
        self.__recordPaginator = RecordPaginator(self.__options, self.__maxOptionLineCount)

    # Utility Methods

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

    def upKeyPressed(self):
        if not self.__recordPaginator.isFirstRecordOnFirstPage():
            self.__recordPaginator.moveToPreviousRecord()
            self.display()

    def downKeyPressed(self):
        if not self.__recordPaginator.isLastRecordOnLastPage():
            self.__recordPaginator.moveToNextRecord()
            self.display()

    def enterKeyPressed(self):
        self.__setValue()
        self.__recordPaginator.setActiveIndex(-1)
        self.display()
        return True

    def multiChoiceOptionSelected(self):
        selectedOption = self.__recordPaginator.getActiveRecord()
        if not self.__isMultiSelect:
            self.__selectedOptions.clear()
        if not self.__isOptionSelected(selectedOption):
            self.__selectedOptions.append(selectedOption)
        else:
            ListUtil.removeElementByKey(self.__selectedOptions, 'id', selectedOption['id'])
        self.display()

    def quitKeyPressed(self):
        return False

    # Getter Methods

    def getUserInput(self) -> object:
        self._printArea.listenUserSelection(self)
        self.display()
        return self.getValue()

    def getCalculatedHeight(self) -> int:
        return len(self.__options) + 3 + self._fieldValidationErrors.getErrorCount()

    # Private Methods

    def __printOptions(self):
        y = self.__getErrorLineCount() + 2
        # Print Previous Page Icon
        iconStr = ''
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
        iconStr = ''
        if self.__recordPaginator.hasNextPage():
            iconStr = StrUtil.getAlignedAndLimitedStr(u' \u25BC ', self.__width, 'center')
        self._printArea.printText(3, y, iconStr)

    def __getErrorLineCount(self) -> int:
        errorCount = self._fieldValidationErrors.getErrorCount()
        if errorCount > self.__maxErrorLineCount:
            return self.__maxErrorLineCount
        return errorCount

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
