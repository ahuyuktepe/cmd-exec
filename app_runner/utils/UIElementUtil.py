from xml.etree.ElementTree import Element
from app_runner.classes.UIPrintArea import UIPrintArea
from app_runner.ui_elements.UIElement import UIElement
from app_runner.ui_elements.UILabel import UIText
from app_runner.utils.XmlElementUtil import XmlElementUtil


class UIElementUtil:

    @staticmethod
    def builUIElementsFromXmlElement(element: Element, parent: UIElement) -> list:
        elements: list = []
        for child in element:
            if child.tag == 'text':
                uiElement = UIElementUtil.buildTextElement(child, parent)
                elements.append(uiElement)
        return elements

    @staticmethod
    def buildTextElement(element: Element, parent: UIElement) -> UIText:
        id = XmlElementUtil.getAttrValueAsStr(element, 'id', 'lbl')
        label = UIText(id)
        label.setAttributes(element)
        # Set Printer
        sectionPrintArea: UIPrintArea = parent.getPrintArea()
        label.setPrintArea(sectionPrintArea)
        return label
