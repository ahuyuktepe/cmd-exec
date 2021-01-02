from src.config.AppConfigPath import AppConfigPath
from src.util.StrUtil import StrUtil


class AppConfigs:
    __configs: dict

    def __init__(self):
        self.__configs = {}

    # Setter Methods

    def addConfig(self, props: dict):
        if props is not None:
            self.__configs.update(props)

    # Getter Methods

    def getValue(self, keyPath: str = None) -> object:
        if StrUtil.isNoneOrEmpty(keyPath):
            return self.__configs
        elif not isinstance(keyPath, str):
            return None
        configPath = AppConfigPath(keyPath)
        return self.__getValueByPath(configPath)

    # Private Methods

    def __getValueByPath(self, configPath: AppConfigPath) -> object:
        if not configPath.hasNextName():
            return self.__configs.get(configPath.getCurrentName())
        name = configPath.getCurrentName()
        value = self.__configs.get(name)
        return self.__getNestedValueByPath(configPath, value)

    def __getNestedValueByPath(self, configPath: AppConfigPath, value: object) -> object:
        if not configPath.hasNextName():
            return value
        elif not isinstance(value, dict):
            return None
        configPath.nextName()
        name = configPath.getCurrentName()
        value = value.get(name)
        return self.__getNestedValueByPath(configPath, value)
