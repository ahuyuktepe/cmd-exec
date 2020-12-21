from app_runner.menu.Command import Command
from app_runner.services.BaseService import BaseService


class UIService(BaseService):

    # Utility Methods

    def getSelectedCommand(self, data: dict = {}) -> Command:
        cmd: Command = self.__screen.getSelectedCommand(data)
        return cmd

    def collectCmdArguments(self, cmd: Command) -> dict:
        values: dict = self.__screen.collectFieldValues(cmd)
        return values

    def displayXml(self, htmlText: str):
        self.__screen.displayXml(htmlText)

    def displayView(self, vid: str, data: dict = {}):
        self.__screen.displayView(vid, data)
