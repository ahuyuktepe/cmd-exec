from xml.etree.ElementTree import Element

from app_runner.app.context.AppContext import AppContext
from app_runner.ui.terminal.element.UIElement import UIElement
from app_runner.ui.terminal.utils.XmlElementUtil import XmlElementUtil
from app_runner.utils.StrUtil import StrUtil


class LabelElement(UIElement):
    __text: str
    __align: str

    def __init__(self, id: str, appContext: AppContext):
        super().__init__(id, 'label', appContext)

    # Setter Functions

    def setText(self, text: str):
        self.__text = text

    def setAttributes(self, element: Element):
        # Set Common Attributes
        super().setAttributes(element)
        # Set Label Attributes
        self.__align = XmlElementUtil.getAttrValueAsStr(element, 'align', 'left')
        self.setText(element.text)
        # Set Location Attributes
        parent = self.getParent()
        x = XmlElementUtil.calculateX(element, parent.getWidth(), parent.getCols(), self.getColSpan())
        y = XmlElementUtil.calculateY(element, parent.getHeight(), parent.getRows(), self.getRowSpan())
        self.setLocation(x, y)
        # Set Dimension Attributes
        width = XmlElementUtil.calculateWidth(element, parent.getWidth(), parent.getCols())
        height = XmlElementUtil.calculateHeight(element, parent.getHeight(), parent.getRows())
        self.setDimensions(width, height)

    # Utility Methods

    def print(self):
        text = StrUtil.getAlignedAndLimitedStr(self.__text, self.getWidth()-1, self.__align)
        self._window.addstr(self._y, self._x, text)
        self.refresh()

    def setListeners(self):
        pass

    def clearListeners(self):
        pass
