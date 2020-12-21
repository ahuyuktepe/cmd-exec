import curses


class UIPrintArea:
    __window: object
    _x: int
    _y: int
    _width: int
    _height: int

    def __init__(self, window: object, x: int, y: int, width: int, height: int):
        self.__window = window
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    # Getter Methods

    def getUserInputAsChar(self) -> object:
        curses.cbreak()
        curses.noecho()
        input = self.__window.get_wch()
        return input

    def getUserInputAsStr(self, x: int, y: int) -> object:
        curses.echo()
        input = self.__window.getstr(y, x)
        curses.noecho()
        return input.decode('utf-8')

    def getX(self) -> int:
        return self._x

    def getY(self) -> int:
        return self._y

    def getWidth(self) -> int:
        return self._width

    def getHeight(self) -> int:
        return self._height

    def getWindow(self) -> object:
        return self.__window

    # Flow Methods

    def printText(self, x: int, y: int, text: str, colorCode: int = 0):
        self.__window.addstr(y, x, text, curses.color_pair(colorCode))

    def printLine(self, x: int, y: int, width: int):
        self.__window.hline(y, x, curses.ACS_HLINE, width)

    def addBorder(self):
        self.__window.border()

    def refresh(self):
        return self.__window.refresh()

    def clear(self):
        return self.__window.clear()
