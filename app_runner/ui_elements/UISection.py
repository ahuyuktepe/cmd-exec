from app_runner.ui_elements.UIElement import UIElement


class UISection(UIElement):
    __elements: list

    def __init__(self, sid: str):
        super().__init__(sid, 'section')
        self.__elements = []

    # Setter Methods

    def addElement(self, element: UIElement):
        if element is not None:
            self.__elements.append(element)

    # Flow Methods

    def display(self):
        self._printArea.addBorder()
        for element in self.__elements:
            element.display()
            element.listenEvents()

    # ============= Code To Be Enabled ==============

    # def getFirstElementByType(self, type: str) -> UIElement:
    #     for element in self.__elements:
    #         if element.getType() == type:
    #             return element
    #     return None

    # def setElements(self, elements: list):
    #     self.__elements = elements