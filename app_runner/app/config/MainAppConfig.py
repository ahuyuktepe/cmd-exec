from app_runner.app.config.AppConfig import AppConfig
from app_runner.utils.ListUtil import ListUtil


class MainAppConfig(AppConfig):

    def __init__(self, configs: dict):
        super().__init__(configs)

    def getCommandLocator(self, cid: str) -> dict:
        commands: list = self.getObjValue('commands')
        return ListUtil.getElementByKey(commands, 'cid', cid)

    def getDefaultArgsByCommand(self, cid: str) -> dict:
        cmdLocator = self.getCommandLocator(cid)
        arguments = cmdLocator.get('arguments')
        if arguments is not None:
            return arguments
        return {}
