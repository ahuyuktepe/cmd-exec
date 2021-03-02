from src.config.AppConfigs import AppConfigs
from src.service.AppService import AppService


class TestService4(AppService):
    __appConfigs: AppConfigs

    def __init__(self, appConfigs: AppConfigs):
        self.__appConfigs = appConfigs

    def getAppName(self) -> str:
        return str(self.__appConfigs.getValue('application.name'))
