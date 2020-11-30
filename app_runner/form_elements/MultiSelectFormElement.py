import curses
from app_runner.enums.UIColor import UIColor
from app_runner.field.MultiSelectField import MultiSelectField
from app_runner.form_elements.FormUIElement import FormUIElement
from app_runner.services.FieldService import FieldService
from app_runner.utils.StrUtil import StrUtil


class MultiSelectFormElement(FormUIElement):
    __options: list
    __activeIndex: int
    __selectedIndices: []

    def __init__(self, field: MultiSelectField, mid: str, fieldService: FieldService):
        super().__init__(field, mid, fieldService)
        self.__options = field.getOptions()
        self.__activeIndex = -1
        self.__selectedIndices = []
        self._value = []

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

    # Getter Methods

    def getUserInput(self) -> object:
        self.__listenUserInput()
        self.display()
        return self.getValue()

    def getCalculatedHeight(self) -> int:
        return len(self.__options) + 3 + self._fieldValidationErrors.getErrorCount()

    # Private Methods

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
                if self.__activeIndex not in self.__selectedIndices:
                    self.__selectedIndices.append(self.__activeIndex)
                else:
                    self.__selectedIndices.remove(self.__activeIndex)
                self.display()
            elif input == 'e':
                curses.unget_wch('q')
                self.__activeIndex = -1
                self.__setValues()
                self.display()

    def __printOptions(self):
        for i in range(0, len(self.__options)):
            x = i + self._fieldValidationErrors.getErrorCount() + 2
            option = self.__options[i]
            label = option['label']
            if self.__activeIndex == i:
                self._printArea.printText(3, x, self.__getOptionLabel(label, i), UIColor.ACTIVE_COMMAND_COLOR)
            else:
                self._printArea.printText(3, x, self.__getOptionLabel(label, i))

    def __getOptionLabel(self, label: str, currentIndex: int) -> str:
        retStr = '['
        if currentIndex in self.__selectedIndices:
            retStr += '*'
        else:
            retStr += ' '
        retStr += '] ' + label
        return retStr

    def __increaseActiveIndexAndPrint(self):
        if self.__activeIndex < len(self.__options) - 1:
            self.__activeIndex += 1
            self.display()

    def __decreaseActiveIndexAndPrint(self):
        if self.__activeIndex > 0:
            self.__activeIndex -= 1
            self.display()

    def __setValues(self):
        for index in self.__selectedIndices:
            option = self.__options[index]
            self._value.append(option.get('id'))
