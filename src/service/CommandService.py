from src.menu.Command import Command
from src.service.AppService import AppService


class CommandService(AppService):

    def buildCmdFromId(self, cid: str) -> Command:
        pass
