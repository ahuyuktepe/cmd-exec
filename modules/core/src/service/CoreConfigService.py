from src.config.AppConfigs import AppConfigs
from src.log.LogSettings import LogSettings
from src.service.ConfigService import ConfigService


class CoreConfigService(ConfigService):
    __configs: AppConfigs

    def __init__(self, configs: AppConfigs):
        self.__configs = configs

    def getModeIds(self) -> list:
        modes = self.__configs.getValue('application.modes')
        retList = []
        for props in modes:
            retList.append(props.get('id'))
        return retList

    def getModePropsById(self, mid: str) -> dict:
        modes = self.__configs.getValue('application.modes')
        for props in modes:
            modId = props.get('id')
            if modId == mid:
                return props
        return None

    def getLogSettings(self) -> LogSettings:
        settings = self.__configs.getValue('log_settings')
        return LogSettings(settings)
