from src.config.AppConfigs import AppConfigs
from src.service.AppService import AppService


class TestConfigService(AppService):
    __configs: AppConfigs

    def __init__(self, configs: AppConfigs):
        self.__configs = configs

    def getName(self) -> str:
        return str(self.__configs.getValue('application.name'))
