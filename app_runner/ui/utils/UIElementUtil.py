from xml.etree.ElementTree import Element

from app_runner.ui.classes.TerminalPrintArea import TerminalPrintArea
from app_runner.ui.element.UISection import UISection
from app_runner.ui.element.UIView import UIView
from app_runner.ui.terminal.element.UIElement import UIElement
from app_runner.ui.utils.XmlElementUtil import XmlElementUtil


class UIElementBuilder:

    @staticmethod
    def buildView(vid: str, element: Element) -> UIView:
        # Initialize View
        id = XmlElementUtil.getAttrValueAsStr(element, 'id', vid)
        view: UIView = UIView(id)
        view.setAttributes(element)
        return view

    @staticmethod
    def buildSectionInView(element: Element, view: UIView) -> UISection:
        id = XmlElementUtil.getAttrValueAsStr(element, 'id')
        section = UISection(id)
        section.setAttributes(element)
        # Set Dimensions
        x = XmlElementUtil.getAttrValueAsInt(element, 'x', 0)
        y = XmlElementUtil.getAttrValueAsInt(element, 'y', 0)
        width = XmlElementUtil.getAttrValueAsInt(element, 'width', view.getWidth())
        height = XmlElementUtil.getAttrValueAsInt(element, 'height', view.getHeight())
        # Set Printer
        viewPrintArea: TerminalPrintArea = view.getPrintArea()
        sectionPrintArea: TerminalPrintArea = TerminalPrintArea()
        sectionPrintArea.initializeDerived(x, y, width, height, viewPrintArea.getWindow())
        section.setPrintArea(sectionPrintArea)
        return section

