from xml.etree.ElementTree import Element
from app_runner.ui.terminal.element.UIElement import UIElement
from app_runner.ui.element.UISection import UISection


class UIView(UIElement):
    __sections: list

    def __init__(self, id: str):
        super().__init__(id, 'view')
        self.__sections = []

    # Setter Methods
    def setAttributes(self, element: Element):
        super().setAttributes(element)

    def addSection(self, section: UISection):
        if section is not None:
            self.__sections.append(section)

    def setSections(self, sections: list):
        self.__sections = sections

    # Utility Methods

    def display(self):
        if self.hasBorder():
            self._printArea.addBorder()
        for section in self.__sections:
            section.display()
        self.refresh()
