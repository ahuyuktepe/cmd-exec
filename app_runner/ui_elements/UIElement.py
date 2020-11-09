from xml.etree.ElementTree import Element
from app_runner.app.context.AppContext import AppContext
from app_runner.classes import UIPrintArea
from app_runner.utils.XmlElementUtil import XmlElementUtil


class UIElement:
    _id: str
    _type: str
    _withBorder: bool
    _printArea: UIPrintArea
    _x: int
    _y: int

    def __init__(self, id: str, type: str):
        self._id = id
        self._type = type
        self._withBorder = False

    # Getter Functions

    def getWidth(self) -> int:
        return self._printArea.getWidth()

    def getHeight(self) -> int:
        return self._printArea.getHeight()

    def getId(self) -> str:
        return self._id

    def getType(self) -> str:
        return self._type

    def getAppContext(self) -> AppContext:
        return self._appContext

    def getPrintArea(self) -> UIPrintArea:
        return self._printArea

    def hasBorder(self) -> bool:
        return self._withBorder

    def toString(self):
        print('type: ' + self._type + ' | id: ' + self._id + ' | x: ' + str(self._x) + ' | y: ' + str(self._y) + ' width: ' + str(self._width) + ' | height: ' + str(self._height))

    # Setter Methods

    def setAttributes(self, element: Element):
        self._withBorder = XmlElementUtil.getAttrValueAsBool(element, 'border', False)
        self._x = XmlElementUtil.getAttrValueAsInt(element, 'x', 1)
        self._y = XmlElementUtil.getAttrValueAsInt(element, 'y', 1)

    def setPrintArea(self, printArea: UIPrintArea):
        self._printArea = printArea

    # Utility Methods

    def display(self):
        pass

    def destroy(self):
        self._printArea.clear()
        self._printArea.refresh()

    def initialize(self):
        pass

    def setListeners(self):
        pass

    def setWithBorder(self, withBorder: bool):
        self._withBorder = withBorder

    def clear(self):
        self._printArea.clear()

    def refresh(self):
        self._printArea.refresh()
