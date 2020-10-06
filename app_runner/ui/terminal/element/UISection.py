import curses
from xml.etree.ElementTree import Element

from app_runner.app.context.AppContext import AppContext
from app_runner.ui.terminal.element.UIElement import UIElement
from app_runner.ui.terminal.utils.XmlElementUtil import XmlElementUtil


class UISection(UIElement):
    __elements: list
    __cols: int
    __rows: int

    def __init__(self, sid: str, appContext: AppContext):
        super().__init__(sid, 'section', appContext)
        self.__elements = []

    # Setter Methods

    def addElement(self, element: UIElement):
        if element is not None:
            self.__elements.append(element)

    def setAttributes(self, element: Element):
        super(UISection, self).setAttributes(element)
        parent = self.getParent()
        width = XmlElementUtil.getAttrValueAsInt(element, 'width', parent.getWidth())
        height = XmlElementUtil.getAttrValueAsInt(element, 'height', parent.getHeight())
        self.setDimensions(width, height)
        self.setLocation(0, 0)
        self.__cols = XmlElementUtil.getAttrValueAsInt(element, 'cols', 1)
        self.__rows = XmlElementUtil.getAttrValueAsInt(element, 'rows', 1)
        super().setAttributes(element)

    # Getter Methods

    def getCols(self) -> int:
        return self.__cols

    def getRows(self) -> int:
        return self.__rows

    # Utility Methods

    def initialize(self):
        self._window = curses.newwin(self._height, self._width, self._y, self._x)

    def print(self):
        element: UIElement
        for element in self.__elements:
            element.print()
            element.setup()
        self.displayBorder()
        self.refresh()
