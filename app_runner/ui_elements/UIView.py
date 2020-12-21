from app_runner.events.EventManager import EventManager
from app_runner.ui_elements.UIElement import UIElement
from app_runner.ui_elements.UISection import UISection


class UIView(UIElement):
    __sections: list

    def __init__(self, id: str):
        super().__init__(id, 'view')
        self.__sections = []

    # Getter Methods

    def getLastSection(self) -> UISection:
        return self.__sections[-1]

    def getSections(self) -> list:
        return self.__sections

    # Setter Methods

    def addSection(self, section: UISection):
        if section is not None:
            self.__sections.append(section)

    # Flow Methods

    def display(self):
        self._printArea.addBorder()
        for section in self.__sections:
            section.display()
            section.listenEvents()
        self.listenEvents()
        self.refresh()

    def destroy(self):
        self.clear()
        self.refresh()
        EventManager.clearListeners()

    # ============= Code To Be Enabled ==============

    # def addUIElement(self, element: UIElement):
    #     self.__uiElements.append(element)

    # def getFirstElementByType(self, type: str) -> UIElement:
    #     for section in self.__sections:
    #         element = section.getFirstElementByType(type)
    #         if element is not None:
    #             return element
    #     return None

    # def getSelectedUIElement(self) -> UIElement:
    #     if self.__selectedIndex >= 0:
    #         return self.__uiElements[self.__selectedIndex]
    #     return None

    # def hasUIElements(self) -> bool:
    #     return len(self.__uiElements) > 0

    # def focusOnNextElement(self, data={}):
    #     elementCount = len(self.__uiElements)
    #     if elementCount > 1:
    #         # Unfocus On Current Selected Element
    #         uiElement = self.getSelectedUIElement()
    #         uiElement.unfocus()
    #         EventManager.removeListenersForElement(uiElement.getId(), KeyEventType.getAll())
    #         # Focus on Next Element
    #         self.__selectNextElement()
    #         self.__focusOnSelectedElement()

    # def __focusOnSelectedElement(self):
    #     # Focus Element
    #     uiElement = self.getSelectedUIElement()
    #     if uiElement is not None:
    #         uiElement.focus()
    #         EventManager.listenEvents(KeyEventType.getAll(), uiElement)

    # def __selectNextElement(self):
    #     elementCount = len(self.__uiElements)
    #     nextIndex = self.__selectedIndex + 1
    #     if nextIndex == elementCount:
    #         nextIndex = 0
    #     self.__selectedIndex = nextIndex
