from app_runner.ui.terminal.element.UIElement import UIElement


class LabelUIElement(UIElement):
    __text: str

    def __init__(self, id: str, text: str):
        super().__init__(id, 'label')
        self.__text = text

    def getText(self) -> str:
        return self.__text

    def getDisplayText(self) -> str:
        return self.__text

    def print(self, window):
        window.addstr(self._y, self._x, self.getDisplayText())
