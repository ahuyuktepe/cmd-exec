from xml.etree.ElementTree import Element
from app_runner.ui_elements.UIElement import UIElement
from app_runner.utils.XmlElementUtil import XmlElementUtil


class UISection(UIElement):
    __elements: list
    __hasBorder: bool

    def __init__(self, sid: str):
        super().__init__(sid, 'section')
        self.__elements = []

    # Getter Methods

    def getFirstElementByType(self, type: str) -> UIElement:
        for element in self.__elements:
            if element.getType() == type:
                return element
        return None

    def hasBorder(self) -> bool:
        return self.__hasBorder

    # Setter Methods

    def addElement(self, element: UIElement):
        if element is not None:
            self.__elements.append(element)

    def setElements(self, elements: list):
        self.__elements = elements

    def setAttributes(self, element: Element):
        self.__hasBorder = XmlElementUtil.getAttrValueAsBool(element, 'border', True)

    def setX(self, x: int):
        self._x = x

    def setY(self, y: int):
        self._y = y

    # Flow Methods

    def display(self):
        if self.hasBorder():
            self._printArea.addBorder()
        for element in self.__elements:
            element.display()
            element.listenEvents()
