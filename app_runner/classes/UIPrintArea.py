import curses


class UIPrintArea:
    __window: object
    _width: int
    _height: int

    def __init__(self, window: object, width: int, height: int):
        self.__window = window
        self._width = width
        self._height = height

    def printText(self, x: int, y: int, text: str, colorCode: int = 1):
        self.__window.addstr(y, x, text, colorCode)

    def printLine(self, x: int, y: int, width: int):
        self.__window.hline(y, x, curses.ACS_HLINE, width)

    def addBorder(self):
        self.__window.border()

    def refresh(self):
        return self.__window.refresh()

    def clear(self):
        return self.__window.clear()

    # Getter Methods

    def getUserInput(self) -> object:
        curses.cbreak()
        curses.noecho()
        input = self.__window.get_wch()
        return input

    def getWidth(self) -> int:
        return self._width

    def getHeight(self) -> int:
        return self._height

    def getWindow(self) -> object:
        return self.__window
