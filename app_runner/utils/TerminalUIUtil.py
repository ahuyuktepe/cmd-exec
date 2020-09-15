import math

from app_runner.menu.Menu import Menu
from app_runner.ui.terminal.element.LabelUIElement import LabelUIElement
from app_runner.ui.terminal.element.UIMenuElement import UIMenuElement
from app_runner.ui.terminal.screen.UISection import UISection


class TerminalUIUtil:

    @staticmethod
    def buildSection(id: str, x: int, y: int, width: int, height: int) -> UISection:
        section: UISection = UISection(id, 'section')
        section.setDimensions(width, height)
        section.setLocation(x, y)
        section.initialize()
        return section

    @staticmethod
    def addLabelToSection(section: UISection, id: str, label: str, x: int, y: int, width: int, height: int):
        labelElement = LabelUIElement(id, label)
        labelElement.setLocation(x, y)
        labelElement.setDimensions(width, height)
        section.addElement(labelElement)

    @staticmethod
    def buildMenuElementForSection(section: UISection, menu: Menu) -> UIMenuElement:
        width = 60
        height = 15
        x = math.floor((section.getWidth() - width) / 2)
        y = math.floor((section.getHeight() - height) / 2)
        element: UIMenuElement = UIMenuElement(
            id=menu.getId(),
            menu=menu
        )
        element.setLocation(x, y)
        element.setDimensions(width, height)
        return element
