from app_runner.ui.terminal.element.LabelUIElement import LabelUIElement
from app_runner.ui.terminal.screen.UISection import UISection


class TerminalUIUtil:

    @staticmethod
    def buildSection(id: str, type: str, title: str, x: int, y: int, width: int, height: int) -> UISection:
        section: UISection = UISection(id, type, title)
        section.setDimensions(width, height)
        section.setLocation(x, y)
        section.initialize()
        return section

    @staticmethod
    def printLabelElement(section: UISection, element: LabelUIElement):
        pass
