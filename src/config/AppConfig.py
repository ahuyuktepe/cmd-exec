from src.config.AppConfigPath import AppConfigPath
from src.utils.StrUtil import StrUtil


class AppConfig:
    __configs: dict

    def __init__(self, configs: dict):
        self.__configs = configs

    def getObjValue(self, path: str = None) -> object:
        if StrUtil.isNoneOrEmpty(path):
            return self.__configs
        elif not isinstance(path, str):
            return None
        return self.__getValueByPath(AppConfigPath(path))

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
