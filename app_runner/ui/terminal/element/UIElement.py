import curses
from xml.etree.ElementTree import Element

from app_runner.app.context.AppContext import AppContext
from app_runner.ui.terminal.utils.XmlElementUtil import XmlElementUtil


class UIElement:
    _window: object
    _appContext: AppContext
    _id: str
    _type: str
    _x: int
    _y: int
    _width: int
    _height: int
    _withBorder: bool
    _parent: object
    _colSpan: int
    _rowSpan: int

    def __init__(self, id: str, type: str, appContext: AppContext):
        self._id = id
        self._type = type
        self._withBorder = False
        self._appContext = appContext

    # Getter Functions

    def getWindow(self) -> object:
        return self._window

    def getDerivedWindow(self, x: int, y: int, width: int, height: int):
        return self._window.derwin(height, width, y, x)

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

    def getParent(self) -> object:
        return self._parent

    def getColSpan(self) -> int:
        return self._colSpan

    def getRowSpan(self) -> int:
        return self._rowSpan

    def hasBorder(self) -> bool:
        return self._withBorder

    def toString(self):
        print('type: ' + self._type + ' | id: ' + self._id + ' | x: ' + str(self._x) + ' | y: ' + str(self._y) + ' width: ' + str(self._width) + ' | height: ' + str(self._height))

    # Setter Methods

    def setParent(self, parent: object):
        self._parent = parent

    def setWindow(self, window):
        self._window = window

    def setDimensions(self, width: int, height: int):
        self._width = width
        self._height = height

    def setLocation(self, x: int, y: int):
        self._x = x
        self._y = y

    def setAttributes(self, element: Element):
        self._withBorder = XmlElementUtil.getAttrValueAsBool(element, 'border')
        self._colSpan = XmlElementUtil.getAttrValueAsInt(element, 'colspan', 1)
        self._rowSpan = XmlElementUtil.getAttrValueAsInt(element, 'rowspan', 1)

    def setY(self, y: int):
        self._y = y

    # Utility Methods

    def displayBorder(self):
        if self._withBorder:
            self._window.border()

    def print(self):
        pass

    def initialize(self):
        self._window = curses.newwin(self._height, self._width, self._y, self._x)

    def clear(self):
        self._window.clear()

    def refresh(self):
        self._window.refresh()

    def moveCursor(self, x: int, y: int):
        self._window.move(y, x)

    def setListeners(self):
        pass

    def setup(self):
        self.setListeners()

    def destroy(self):
        pass
