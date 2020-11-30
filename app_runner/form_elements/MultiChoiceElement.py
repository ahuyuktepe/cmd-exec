import curses

from app_runner.enums.UIColor import UIColor
from app_runner.field.Field import Field
from app_runner.form_elements.FormUIElement import FormUIElement
from app_runner.services.FieldService import FieldService
from app_runner.utils.StrUtil import StrUtil


class MultiChoiceElement(FormUIElement):
    __options: list
    __activeIndex: int
    __selectedIndexes: list
    __isMultiSelect: bool

    def __init__(self, field: Field, mid: str, fieldService: FieldService, isMultiSelect: bool = False):
        super().__init__(field, mid, fieldService)
        self.__options = field.getOptions()
        self.__activeIndex = -1
        self.__selectedIndexes = []
        self.__isMultiSelect = isMultiSelect
        self._value = []

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

    # Getter Methods

    def getUserInput(self) -> object:
        self.__listenUserInput()
        self.__setValues()
        self.display()
        return self.getValue()

    def getValue(self) -> str:
        selectedOptionIds = self.getSelectedOptionIds()
        return '|'.join(selectedOptionIds)

    def getSelectedOptionIds(self) -> list:
        optionIds: list = []
        if self.isSelected():
            for option in self._value:
                optionIds.append(option['id'])
        return optionIds

    def getCalculatedHeight(self) -> int:
        return len(self.__options) + 3 + self._fieldValidationErrors.getErrorCount()

    # Private Methods

    def __setValues(self):
        self._value.clear()
        for index in self.__selectedIndexes:
            option = self.__options[index]
            self._value.append(option)

    def __listenUserInput(self):
        self.__activeIndex = 0
        self.display()
        curses.cbreak()
        curses.noecho()
        input = None
        while input != 'q':
            input = self._printArea.getUserInputAsChar()
            if input == 'w':
                self.__decreaseActiveIndexAndPrint()
            elif input == 's':
                self.__increaseActiveIndexAndPrint()
            elif input == ' ':
                self.__selectActiveIndex()
                self.display()
            elif input == 'e':
                if self.isSelected():
                    curses.unget_wch('q')
                    self.__activeIndex = -1
                    self.display()

    def __selectActiveIndex(self):
        if not self.__isMultiSelect:
            self.__selectedIndexes.clear()
        if not self.isActiveIndexSelected():
            self.__selectedIndexes.append(self.__activeIndex)
        else:
            self.__selectedIndexes.remove(self.__activeIndex)

    def isActiveIndexSelected(self):
        return self.__activeIndex in self.__selectedIndexes

    def __increaseActiveIndexAndPrint(self):
        if self.__activeIndex < len(self.__options) - 1:
            self.__activeIndex += 1
            self.display()

    def __decreaseActiveIndexAndPrint(self):
        if self.__activeIndex > 0:
            self.__activeIndex -= 1
            self.display()

    def __printOptions(self):
        for i in range(0, len(self.__options)):
            x = i + self._fieldValidationErrors.getErrorCount() + 2
            option = self.__options[i]
            label = option['label']
            if self.__activeIndex == i:
                self._printArea.printText(3, x, self.__getOptionLabel(label, i), UIColor.ACTIVE_COMMAND_COLOR)
            elif i in self.__selectedIndexes:
                self._printArea.printText(3, x, self.__getOptionLabel(label, i), UIColor.SUCCESS_MESSAGE_COLOR)
            else:
                self._printArea.printText(3, x, self.__getOptionLabel(label, i))

    def __getOptionLabel(self, label: str, currentIndex: int) -> str:
        retStr = '['
        if currentIndex in self.__selectedIndexes:
            retStr += '*'
        else:
            retStr += ' '
        retStr += '] ' + label
        return retStr