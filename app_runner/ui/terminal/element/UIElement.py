

class UIElement:
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

    def setDimensions(self, width: int, height: int):
        self._width = width
        self._height = height

    def setLocation(self, x: int, y: int):
        self._x = x
        self._y = y

    def print(self, window):
        print('print element')

    # Getter Functions
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

    def toString(self):
        print('x: ' + str(self._x) + ' | y: ' + str(self._y) + ' width: ' + str(self._width) + ' | height: ' + str(self._height))
