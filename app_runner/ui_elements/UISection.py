from xml.etree.ElementTree import Element
from app_runner.ui_elements.UIElement import UIElement
from app_runner.utils.XmlElementUtil import XmlElementUtil


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

    def setElements(self, elements: list):
        self.__elements = elements

    def setAttributes(self, element: Element):
        super().setAttributes(element)
        self.__cols = XmlElementUtil.getAttrValueAsInt(element, 'cols', 1)
        self.__rows = XmlElementUtil.getAttrValueAsInt(element, 'rows', 1)

    # Getter Methods

    def getBottomY(self) -> int:
        y = 0
        for section in self.__elements:
            y += section.getPrintArea().getHeight() - 1
        return y

    def getCols(self) -> int:
        return self.__cols

    def getRows(self) -> int:
        return self.__rows

    # Utility Methods

    def display(self):
        self._printArea.addBorder()
        for element in self.__elements:
            element.display()
            element.setListeners()

    def destroy(self):
        for element in self.__elements:
            element.destroy()
        self.clear()
