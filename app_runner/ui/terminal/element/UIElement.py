from xml.etree.ElementTree import Element
from app_runner.app.context.AppContext import AppContext
from app_runner.ui.classes import TerminalPrintArea
from app_runner.ui.utils.XmlElementUtil import XmlElementUtil


class UIElement:
    _appContext: AppContext
    _id: str
    _type: str
    _withBorder: bool
    _printArea: TerminalPrintArea

    def __init__(self, id: str, type: str):
        self._id = id
        self._type = type

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

    def getPrintArea(self) -> TerminalPrintArea:
        return self._printArea

    def hasBorder(self) -> bool:
        return self._withBorder

    def toString(self):
        print('type: ' + self._type + ' | id: ' + self._id + ' | x: ' + str(self._x) + ' | y: ' + str(self._y) + ' width: ' + str(self._width) + ' | height: ' + str(self._height))

    # Setter Methods

    def setAttributes(self, element: Element):
        print('set element attributes: ' + self._id)
        self._withBorder = XmlElementUtil.getAttrValueAsBool(element, 'border', False)

    def setPrintArea(self, printArea: TerminalPrintArea):
        self._printArea = printArea

    # Utility Methods

    def display(self):
        print('display element: ' + self._id)

    def initialize(self):
        print('initialize element: ' + self._id)

    def clear(self):
        print('clear element: ' + self._id)
        self._printArea.clear()
        self.refresh()

    def refresh(self):
        print('refresh element: ' + self._id)
        self._printArea.refresh()
