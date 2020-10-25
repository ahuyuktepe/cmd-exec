import curses
from app_runner.app.context.AppContext import AppContext
from app_runner.errors.FieldValidationErrors import FieldValidationErrors
from app_runner.field.Field import Field
from app_runner.menu.Command import Command
from app_runner.ui.terminal.enums.UIColor import UIColor
from app_runner.ui.terminal.form.FormUIElement import FormUIElement
from app_runner.utils.StrUtil import StrUtil


class TextElement(FormUIElement):
    def __init__(self, field: Field, appContext: AppContext):
        super().__init__(field, appContext)
        self.__value = ""

    # Utility Methods

    def print(self):
        labelStr = StrUtil.getAlignedAndLimitedStr(self._field.getLabel(), self.getWidth(), 'left')
        self._window.addstr(1, 1, labelStr)
        self.__printValue()
        self.displayBorder()
        self.refresh()

    def getUserInput(self) -> object:
        curses.echo(True)
        curses.nocbreak()
        while True:
            self._value = self._window.getstr(2, 2).decode('utf-8')
            self.__printValue()
            if self.__validateValue():
                break
        return self._value

    # Private Methods

    def __printValue(self):
        if self.__value != '':
            self._window.addstr(2, 2, self.__value, curses.color_pair(UIColor.SUCCESS_MESSAGE_COLOR))
            self.refresh()


