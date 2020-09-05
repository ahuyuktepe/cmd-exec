from app_runner.app.config.AppConfig import AppConfig
from app_runner.app.context.AppContext import AppContext
from app_runner.app.runner.ApplicationRunner import ApplicationRunner
from app_runner.ui.terminal.MainScreen import MainScreen
import time
import curses
from app_runner.ui.terminal.element.LabelUIElement import LabelUIElement
from app_runner.ui.terminal.screen.UISection import UISection
from app_runner.utils.TerminalUIUtil import TerminalUIUtil


class IntAppRunner(ApplicationRunner):

    def __init__(self, context: AppContext):
        super().__init__(context)

    def run(self):
        print('Running in interactive mode')
        screen: MainScreen = self.buildScreen()
        screen.print()
        time.sleep(3)

    def buildScreen(self) -> MainScreen:
        config: AppConfig = self._appContext.getConfig('main')
        appName: str = config.getObjValue('application.name')
        screen: MainScreen = MainScreen(appName)
        screen.initialize()
        self.buildSections(screen)
        return screen

    def buildSections(self, screen: MainScreen):
        screenWidth = screen.getWidth()
        # Header
        section: UISection = TerminalUIUtil.buildSection('header', 'section', 'Header', 0, 0, screenWidth, 3)
        # Application Name Text
        labelElement = LabelUIElement('appName', screen.getTitle())
        labelElement.setLocation(2, 1)
        section.addElement(labelElement)
        # Username Text
        labelElement = LabelUIElement('username', 'ahuyuktepe')
        labelElement.setLocation(screenWidth - 12, 1)
        section.addElement(labelElement)
        screen.addSection(section)

