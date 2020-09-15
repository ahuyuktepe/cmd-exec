from app_runner.menu.Menu import Menu
from app_runner.ui.terminal.element.UIMenuElement import UIMenuElement
from app_runner.ui.terminal.screen.UIScreen import UIScreen
from app_runner.ui.terminal.screen.UISection import UISection
from app_runner.utils.TerminalUIUtil import TerminalUIUtil


class MainScreen(UIScreen):
    __currentY: int = 0
    __menus: list
    __headerSectionId: str = 'header'
    __msgSectionId: str = 'msg'
    __bodySectionId: str = 'body'
    __inputSectionId: str = 'input'
    __helpSectionId: str = 'help'

    def __init__(self, title: str):
        UIScreen.__init__(self, 'main', title)
        self.__menus = []

    def buildSections(self):
        self.__addHeaderSection()
        self.__addMessageSection()
        self.__addBodySection()
        self.__addInputSection()
        self.__addHelpSection()

    # Setter Methods

    def addAndActivateMenu(self, menu: Menu):
        bodySection: UISection = self.getBodySection()
        element = TerminalUIUtil.buildMenuElementForSection(bodySection, menu)
        self.__menus.append(element)
        bodySection.setActiveMenuElement(element)

    def addMenuElement(self, element: UIMenuElement):
        section: UISection = self.getSection(self.__bodySectionId)
        section.addElement(element)

    # Getter Methods

    def getBodySection(self) -> UISection:
        return self.getSection(self.__bodySectionId)

    def getInputSection(self) -> UISection:
        return self.getSection(self.__inputSectionId)

    def getMessageSection(self) -> UISection:
        return self.getSection(self.__inputSectionId)

    def getUserInput(self) -> str:
        inputSection: UISection = self.getInputSection()
        return inputSection.getUserInput()

    # Private Methods

    def __addHeaderSection(self):
        section: UISection = TerminalUIUtil.buildSection(self.__headerSectionId, 0, self.__currentY, self.getWidth(), 3)
        self.__currentY += 2
        TerminalUIUtil.addLabelToSection(section, 'appName', self.getTitle(), 2, 1, 50, 1)
        self.addSection(section)

    def __addMessageSection(self):
        section: UISection = TerminalUIUtil.buildSection(self.__msgSectionId, 0, self.__currentY, self.getWidth(), 3)
        self.__currentY += 2
        self.addSection(section)

    def __addBodySection(self):
        bodyHeight: int = self.getHeight() - 13
        section: UISection = TerminalUIUtil.buildSection(self.__bodySectionId, 0, self.__currentY, self.getWidth(), bodyHeight)
        self.__currentY += bodyHeight - 1
        self.addSection(section)

    def __addInputSection(self):
        section: UISection = TerminalUIUtil.buildSection(self.__inputSectionId, 0, self.__currentY, self.getWidth(), 3)
        self.__currentY += 2
        self.addSection(section)

    def __addHelpSection(self):
        section: UISection = TerminalUIUtil.buildSection(self.__helpSectionId, 0, self.__currentY, self.getWidth(), 4)
        self.__currentY += 3
        TerminalUIUtil.addLabelToSection(section, 'h1', 'q: Quit', 2, 1, 50, 1)
        TerminalUIUtil.addLabelToSection(section, 'h2', 'enter: Select', 2, 2, 50, 1)
        TerminalUIUtil.addLabelToSection(section, 'h3', 'up key: Move Up', 52, 1, 50, 1)
        TerminalUIUtil.addLabelToSection(section, 'h4', 'down key: Move Down', 52, 2, 50, 1)
        self.addSection(section)
