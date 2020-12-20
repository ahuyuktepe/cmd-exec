from xml.etree.ElementTree import Element
from app_runner.events.EventManager import EventManager
from app_runner.events.UIEventType import UIEventType
from app_runner.ui_elements.UIElement import UIElement
from app_runner.ui_elements.UISection import UISection


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

    # Getter Methods

    def getBottomY(self) -> int:
        y = 0
        for section in self.__sections:
            y += section.getPrintArea().getHeight() - 1
        return y

    # Utility Methods

    def display(self):
        if self.hasBorder():
            self._printArea.addBorder()
        for section in self.__sections:
            section.display()
            section.setListeners()
        self.setListeners()
        self.refresh()
        EventManager.triggerEvent(UIEventType.VIEW_LOADED)

    def destroy(self):
        super(UIView, self).destroy()
        self._printArea.clear()
        self._printArea.refresh()
        EventManager.clearListeners()
        for section in self.__sections:
            section.destroy()
