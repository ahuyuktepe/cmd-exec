import curses


class UIPrintArea:
    __window: object
    __isListeningUserInput: bool
    _width: int
    _height: int

    def __init__(self, window: object, width: int, height: int):
        self.__window = window
        self._width = width
        self._height = height
        self.__isListeningUserInput = False

    def printText(self, x: int, y: int, text: str, colorCode: int = 0):
        if colorCode == 0:
            self.__window.addstr(y, x, text)
        else:
            self.__window.addstr(y, x, text, curses.color_pair(colorCode))

    def printLine(self, x: int, y: int, width: int):
        self.__window.hline(y, x, curses.ACS_HLINE, width)

    def addBorder(self):
        self.__window.border()

    def refresh(self):
        return self.__window.refresh()

    def clear(self):
        return self.__window.clear()

    # Utility Methods

    def move(self, x: int, y: int):
        self.__window.mvderwin(y, x)
        self.refresh()

    # Getter Methods

    def getWidth(self) -> int:
        return self._width

    def getHeight(self) -> int:
        return self._height

    def getWindow(self) -> object:
        return self.__window
