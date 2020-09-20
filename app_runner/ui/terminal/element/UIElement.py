import curses


class UIElement:
    _window: object
    _id: str
    _type: str
    _x: int
    _y: int
    _width: int
    _height: int

    def __init__(self, id: str, eType: str):
        self._id = id
        self._type = eType

    # Setter Methods

    def addBorder(self):
        self._window.border()

    def setWindow(self, window):
        self._window = window

    def setDimensions(self, width: int, height: int):
        self._width = width
        self._height = height

    def setLocation(self, x: int, y: int):
        self._x = x
        self._y = y

    def print(self, data: dict = {}):
        self.toString()

    # Getter Functions

    def getWindow(self) -> object:
        return self._window

    def getId(self) -> str:
        return self._id

    def getX(self) -> int:
        return self._x

    def getY(self) -> int:
        return self._y

    def getWidth(self) -> int:
        return self._width

    def getHeight(self) -> int:
        return self._height

    def getType(self) -> str:
        return self._type

    def toString(self):
        print('type: ' + self._type + ' | id: ' + self._id + ' | x: ' + str(self._x) + ' | y: ' + str(self._y) + ' width: ' + str(self._width) + ' | height: ' + str(self._height))

    # Utility Methods

    def initialize(self):
        self._window = curses.newwin(self._height, self._width, self._y, self._x)

    def clear(self):
        self._window.clear()

    def refresh(self):
        self._window.refresh()

    def moveCursor(self, x: int, y: int):
        self._window.move(y, x)
