from src.config.AppConfigs import AppConfigs
from src.error.CmdExecError import CmdExecError
from src.log.LogSettings import LogSettings
from src.service.ConfigService import ConfigService


class CoreConfigService(ConfigService):
    __configs: AppConfigs

    def __init__(self, configs: AppConfigs):
        self.__configs = configs

    def getModeIds(self) -> list:
        modes = self.__configs.getValue('application.modes')
        if modes is None:
            return None
        elif not isinstance(modes, list):
            raise CmdExecError('ERR44')
        retList = []
        for props in modes:
            retList.append(props.get('id'))
        return retList

    def getDefaultMode(self) -> str:
        mode = self.__configs.getValue('application.default_mode')
        if mode is None:
            return None
        elif not isinstance(mode, str):
            raise CmdExecError('ERR42')
        return str(mode)

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
