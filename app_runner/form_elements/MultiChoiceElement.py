import curses
from app_runner.app.context.AppContext import AppContext
from app_runner.field.Field import Field
from app_runner.enums.UIColor import UIColor
from app_runner.form_elements.FormUIElement import FormUIElement
from app_runner.utils.StrUtil import StrUtil


class MultiChoiceElement(FormUIElement):
    __options: list
    __activeIndex: int
    __selectedIndexes: list
    __isMultiSelect: bool

    def __init__(self, field: Field, appContext: AppContext, isMultiSelect: bool = False):
        super().__init__(field, appContext)
        self.__options = field.getOptions()
        self.__activeIndex = -1
        self.__selectedIndexes = []
        self.__isMultiSelect = isMultiSelect

    # Getter Methods

    def getId(self) -> str:
        return self._field.getId()

    def getSelectedOptions(self) -> list:
        optionIds: list = []
        if self.isSelected():
            for index in self.__selectedIndexes:
                optionIds.append(self.__options[index]['id'])
        return optionIds

    def isSelected(self) -> bool:
        return len(self.__selectedIndexes) > 0

    def isActiveIndexSelected(self):
        return self.__activeIndex in self.__selectedIndexes

    # Utility Methods

    def print(self):
        labelStr = StrUtil.getAlignedAndLimitedStr(self._field.getLabel(), self.getWidth(), 'left')
        self.clear()
        self._window.addstr(1, 1, labelStr)
        self.__printOptions()
        self.displayBorder()
        self.refresh()

    def getUserInput(self) -> object:
        self.__listenUserInput()
        selectedOptions = self.getSelectedOptions()
        self.__activeIndex = -1
        self.print()
        return '|'.join(selectedOptions)

    # Private Methods

    def __printOptions(self):
        for i in range(0, len(self.__options)):
            option = self.__options[i]
            label = option['label']
            if self.__activeIndex == i:
                self._window.addstr((i + 2), 3, self.__getOptionLabel(label, i), curses.color_pair(UIColor.ACTIVE_COMMAND_COLOR))
            elif i in self.__selectedIndexes:
                self._window.addstr((i + 2), 3, self.__getOptionLabel(label, i), curses.color_pair(UIColor.SUCCESS_MESSAGE_COLOR))
            else:
                self._window.addstr((i + 2), 3, self.__getOptionLabel(label, i))

    def __listenUserInput(self):
        curses.cbreak()
        curses.noecho()
        input = None
        while input != 'q':
            input = self._window.get_wch()
            if input == 'w':
                self.__decreaseActiveIndexAndPrint()
            elif input == 's':
                self.__increaseActiveIndexAndPrint()
            elif input == ' ':
                self.__selectActiveIndex()
                self.print()
            elif input == 'e':
                self.__validateSelection()
                if self.isSelected():
                    curses.unget_wch('q')

    def __increaseActiveIndexAndPrint(self):
        if self.__activeIndex < len(self.__options) - 1:
            self.__activeIndex += 1
            self.print()

    def __decreaseActiveIndexAndPrint(self):
        if self.__activeIndex > 0:
            self.__activeIndex -= 1
            self.print()

    def __selectActiveIndex(self):
        if not self.__isMultiSelect:
            self.__selectedIndexes.clear()
        if not self.isActiveIndexSelected():
            self.__selectedIndexes.append(self.__activeIndex)
        else:
            self.__selectedIndexes.remove(self.__activeIndex)

    def __getOptionLabel(self, label: str, currentIndex: int) -> str:
        retStr = '['
        if currentIndex in self.__selectedIndexes:
            retStr += '*'
        else:
            retStr += ' '
        retStr += '] ' + label
        return retStr

    def __validateSelection(self):
        if not self.isSelected():
            y = len(self.__options) + 2
            self._window.addstr(y, 1, 'Please select an option', curses.color_pair(UIColor.ERROR_MESSAGE_COLOR))
