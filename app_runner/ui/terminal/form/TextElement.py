import curses
from app_runner.app.context.AppContext import AppContext
from app_runner.field.Field import Field
from app_runner.ui.terminal.form.FormUIElement import FormUIElement
from app_runner.utils.StrUtil import StrUtil


class TextElement(FormUIElement):
    __value: str

    def __init__(self, field: Field, appContext: AppContext):
        super().__init__(field, appContext)
        self.__value = ""

    # Utility Methods

    def print(self):
        labelStr = StrUtil.getAlignedAndLimitedStr(self._field.getLabel(), self.getWidth(), 'left')
        self._window.addstr(1, 1, labelStr)
        if self.__value != '':
            self._window.addstr(2, 1, self.__value)
        self.displayBorder()
        self.refresh()

    def getUserInput(self) -> object:
        curses.echo(True)
        curses.nocbreak()
        self.__value = self._window.getstr(2, 1).decode('utf-8')
        return self.__value
