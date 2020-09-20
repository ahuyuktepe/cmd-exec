from xml.etree.ElementTree import Element
from app_runner.ui.terminal.element.LabelElement import LabelElement
from app_runner.ui.terminal.element.MenuElement import MenuElement
from app_runner.ui.terminal.element.MenuInputElement import MenuInputElement
from app_runner.ui.terminal.element.NavElement import NavElement
from app_runner.ui.terminal.element.UISection import UISection
from app_runner.ui.terminal.utils.XmlElementUtil import XmlElementUtil


class UIElementUtil:
    pass

    @staticmethod
    def buildLabelElementForSection(element: Element, section: UISection) -> LabelElement:
        label = LabelElement('label')
        x = XmlElementUtil.getAttrValueAsInt(element, 'x', 1)
        y = XmlElementUtil.getAttrValueAsInt(element, 'y', 1)
        label.setDimensions(section.getWidth(), 1)
        label.setLocation(x, y)
        label.setText(element.text)
        label.setWindow(section.getWindow())
        return label

    @staticmethod
    def buildNavElementForSection(element: Element, section: UISection) -> NavElement:
        id = XmlElementUtil.getAttrValueAsStr(element, 'id')
        mid = XmlElementUtil.getAttrValueAsStr(element, 'menu')
        nav = NavElement(id, mid)
        nav.setDimensions(section.getWidth(), 1)
        nav.setLocation(1, 1)
        nav.setWindow(section.getWindow())
        return nav

    @staticmethod
    def buildMenuElementForSection(element: Element, section: UISection) -> MenuElement:
        id = XmlElementUtil.getAttrValueAsStr(element, 'id')
        nid = XmlElementUtil.getAttrValueAsStr(element, 'nav')
        menu = MenuElement(id, nid)
        width = XmlElementUtil.getAttrValueAsInt(element, 'width', section.getWidth())
        height = XmlElementUtil.getAttrValueAsInt(element, 'height', section.getHeight())
        menu.setDimensions(width, height)
        x = XmlElementUtil.getAttrValueAsInt(element, 'x', 1)
        y = XmlElementUtil.getAttrValueAsInt(element, 'y', 1)
        menu.setLocation(x, y)
        menu.setWindow(section.getWindow())
        return menu

    @staticmethod
    def buildMenuInputElementForSection(element: Element, section: UISection) -> MenuInputElement:
        id = XmlElementUtil.getAttrValueAsStr(element, 'id')
        input = MenuInputElement(id)
        input.setDimensions(section.getWidth(), 1)
        input.setLocation(2, 1)
        input.setWindow(section.getWindow())
        input.setText(element.text)
        return input
