from xml.etree.ElementTree import Element
from app_runner.ui_elements.UIElement import UIElement
from app_runner.utils.XmlElementUtil import XmlElementUtil


class UILabel(UIElement):
    __text: str
    __align: str
    __size: int

    def __init__(self, id: str):
        super().__init__(id, 'label')

    # Setter Functions

    def setText(self, text: str):
        textSize = len(text)
        if textSize > self.getWidth():
            self.__text = text[:self.getWidth() - 1]
        else:
            self.__text = text

    def setAttributes(self, element: Element):
        self.__align = XmlElementUtil.getAttrValueAsStr(element, 'align', 'left')
        self.setText(element.text)

    # Flow Methods

    def display(self):
        self.print(0, 0, self.__text)

    # ============= Code To Be Enabled ==============

    # def isSelectable(self) -> bool:
    #     return False

    # def updateText(self, data: dict = {}):
    #     text = data.get('text')
    #     self.setText(text)
    #     self.display()
    #     self.refresh()
