import curses
from xml.etree.ElementTree import Element
from app_runner.app.context.AppContext import AppContext
from app_runner.ui.terminal.element.UIElement import UIElement
from app_runner.ui.utils.XmlElementUtil import XmlElementUtil


class UISection(UIElement):
    __elements: list
    __cols: int
    __rows: int

    def __init__(self, sid: str):
        super().__init__(sid, 'section')
        self.__elements = []

    # Setter Methods

    def addElement(self, element: UIElement):
        if element is not None:
            self.__elements.append(element)

    def setAttributes(self, element: Element):
        super().setAttributes(element)
        self.__cols = XmlElementUtil.getAttrValueAsInt(element, 'cols', 1)
        self.__rows = XmlElementUtil.getAttrValueAsInt(element, 'rows', 1)

    # Getter Methods

    def getCols(self) -> int:
        return self.__cols

    def getRows(self) -> int:
        return self.__rows

    # Utility Methods

    def display(self):
        print('print section')
        self._printArea.printText(1, 1, 'Test')
        self._printArea.addBorder()
