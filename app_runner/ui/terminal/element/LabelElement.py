from app_runner.ui.terminal.element.UIElement import UIElement


class LabelElement(UIElement):
    __text: str

    def __init__(self, id: str):
        super().__init__(id, 'label')

    def setText(self, text: str):
        self.__text = text

    def print(self, data: dict = {}):
        self._window.addstr(self._y, self._x, self.__text)
        self.refresh()
