from app_runner.menu.Command import Command
from app_runner.services.BaseService import BaseService
from app_runner.ui_elements.UIScreen import UIScreen


class UIService(BaseService):
    __screen: UIScreen = None

    def setScreen(self, screen: UIScreen):
        self.__screen = screen

    def getSelectedCommand(self, data: dict = {}) -> Command:
        cmd: Command = self.__screen.getSelectedCommand(data)
        return cmd

    def collectCmdArguments(self, cmd: Command) -> dict:
        values: dict = self.__screen.collectFieldValues(cmd)
        return values

    def displayHtml(self, htmlText: str):
        self.__screen.displayHtml(htmlText)

    def displayView(self, vid: str, data: dict = {}):
        self.__screen.displayView(vid, data)
