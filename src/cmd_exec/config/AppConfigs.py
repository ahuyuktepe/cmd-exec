from ..config.ConfigManager import ConfigManager


class AppConfigs:
    __configManager: ConfigManager

    def __init__(self):
        self.__configManager = ConfigManager()

    # Setter Methods

    def addConfig(self, props: dict):
        self.__configManager.save(props)

    def getValue(self, keyPath: str = None) -> object:
        keys: list = keyPath.split('.')
        return self.__configManager.getValue(keys)

    def updateConfigByDict(self, value: dict):
        self.__configManager.updateConfig(value)

    def updateConfigByPath(self, keyPath: str, value: object):
        keys: list = keyPath.split('.')
        self.__configManager.update(keys, value)