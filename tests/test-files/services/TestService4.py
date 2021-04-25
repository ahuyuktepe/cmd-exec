from cmd_exec.config.AppConfigs import AppConfigs
from cmd_exec.service.AppService import AppService


class TestService4(AppService):
    __appConfigs: AppConfigs

    def __init__(self, appConfigs: AppConfigs):
        self.__appConfigs = appConfigs

    def getAppName(self) -> str:
        return str(self.__appConfigs.getValue('application.name'))
