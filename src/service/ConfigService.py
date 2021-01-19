from src.log.LogSettings import LogSettings
from src.service.AppService import AppService


class ConfigService(AppService):

    def getModeIds(self) -> list:
        pass

    def getModePropsById(self, mid: str) -> dict:
        pass

    def getLogSettings(self) -> LogSettings:
        pass
