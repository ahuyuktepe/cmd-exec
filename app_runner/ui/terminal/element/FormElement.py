from xml.etree.ElementTree import Element

from app_runner.app.context.AppContext import AppContext
from app_runner.ui.terminal.element.UIElement import UIElement
from app_runner.ui.terminal.utils.XmlElementUtil import XmlElementUtil


class FormElement(UIElement):

    def __init__(self, id: str, appContext: AppContext):
        super().__init__(id, 'form', appContext)
        self.__setListeners()

    # Setter Methods

    def setAttributes(self, element: Element):
        parent = self.getParent()
        # Set Dimensions
        width = XmlElementUtil.getAttrValueAsInt(element, 'width', parent.getWidth())
        height = XmlElementUtil.getAttrValueAsInt(element, 'height', parent.getHeight())
        self.setDimensions(width, height)
        # Set Locations
        self.setLocation(0, 0)
        super().setAttributes(element)

    # Utility Methods

    def print(self):
        self.refresh()
