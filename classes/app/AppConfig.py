from classes.app.AppConfigPath import AppConfigPath
from classes.errors.InvalidConfigPathError import InvalidConfigPathError
from classes.utils.FileUtil import FileUtil
from classes.utils.StrUtil import StrUtil

class AppConfig:
    __configs: dict

    def __init__(self, configFilePath: str):
        self.__configs = FileUtil.generateObjFromJsonFile(configFilePath)

    def getObjValue(self, path: str) -> object:
        if not isinstance(path, str) or StrUtil.isNoneOrEmpty(path):
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
            raise InvalidConfigPathError()
        configPath.nextName()
        name = configPath.getCurrentName()
        value = value.get(name)
        return self.__getNestedValueByPath(configPath, value)
