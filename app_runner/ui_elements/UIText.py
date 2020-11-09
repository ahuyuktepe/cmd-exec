from xml.etree.ElementTree import Element

from app_runner.errors.UIError import UIError
from app_runner.ui_elements.UIElement import UIElement
from app_runner.utils.XmlElementUtil import XmlElementUtil


class UIText(UIElement):
    __text: str
    __align: str

    def __init__(self, id: str):
        super().__init__(id, 'label')

    # Setter Functions

    def setText(self, text: str):
        self.__text = text

    def setAttributes(self, element: Element):
        # Set Common Attributes
        super().setAttributes(element)
        # Set Label Attributes
        self.__align = XmlElementUtil.getAttrValueAsStr(element, 'align', 'left')
        self.setText(element.text)

    # Utility Methods

    def display(self):
        if self._y > self.getHeight():
            raise UIError("Label '" + self.getId() + "' does not fit into section.")
        self._printArea.printText(self._x, self._y, self.__text)
