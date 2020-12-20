from xml.etree.ElementTree import Element
from app_runner.errors.UIError import UIError
from app_runner.events.EventManager import EventManager
from app_runner.events.UIEventType import UIEventType
from app_runner.ui_elements.UIElement import UIElement
from app_runner.utils.StrUtil import StrUtil
from app_runner.utils.XmlElementUtil import XmlElementUtil


class UILabel(UIElement):
    __text: str
    __size: int
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
        self.__size = XmlElementUtil.getAttrValueAsInt(element, 'size', 10)
        self.__align = XmlElementUtil.getAttrValueAsStr(element, 'align', 'right')
        self.setText(element.text)

    # Utility Methods

    def display(self):
        if self._y > self.getHeight():
            raise UIError("Label '" + self.getId() + "' does not fit into section.")
        x = self._x
        if x < 0:
           x = self.getWidth() + x
        text = StrUtil.getAlignedAndLimitedStr(self.__text, self.__size, self.__align)
        self._printArea.printText(x, self._y, text)

    def setListeners(self):
        EventManager.listenEvent(UIEventType.UPDATE_TEXT, self)

    # Event Listeners

    def updateText(self, data: dict = {}):
        text = data.get('text')
        self.setText(text)
        self.display()
        self.refresh()
