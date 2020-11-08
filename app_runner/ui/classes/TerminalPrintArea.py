import curses


class TerminalPrintArea:
    __screen: object
    __window: object
    _x: int
    _y: int
    _width: int
    _height: int

    def __init__(self):
        self.__window = None
        self.__screen = curses.initscr()

    def printText(self, x: int, y: int, text: str):
        self.__window.addstr(y, x, text)

    def initialize(self, x: int, y: int, width: int, height: int):
        self.__window = curses.newwin(height, width, y, x)

    def initializeDerived(self, x: int, y: int, width: int, height: int, window: object):
        self.__window = window.derwin(height, width, y, x)

    def initializeForFullScreen(self):
        dims: tuple = self.getScreenDimensions()
        self._x = 0
        self._y = 0
        self._width = dims[1]
        self._height = dims[0]
        self.__window = curses.newwin(self._height, self._width, 0, 0)

    def addBorder(self):
        self.__window.border()

    def refresh(self):
        return self.__window.refresh()

    # Getter Methods

    def getScreenDimensions(self) -> tuple:
        return self.__screen.getmaxyx()

    def getWidth(self) -> int:
        return self._width

    def getHeight(self) -> int:
        return self._height

    def getWindow(self) -> object:
        return self.__window
