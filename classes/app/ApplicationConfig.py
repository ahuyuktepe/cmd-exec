from classes.utils.DataUtil import DataUtil
from classes.utils.FileUtil import FileUtil
from classes.utils.StrUtil import StrUtil

class ApplicationConfig:
    __configs: dict

    def __init__(self, configPath: str):
        self.__configs = FileUtil.generateObjFromJsonFile(configPath)

    def getStrValue(self, path: str) -> str:
        return str(self.__getValueByPath(path))

    def getIntValue(self, path: str) -> int:
        value: str = str(self.__getValueByPath(path))
        return StrUtil.strToInt(value)

    def __getValueByPath(self, path: str) -> object:
        if StrUtil.isNoneOrNotString(path):
            return None
        key: str = StrUtil.getFirstStrFromDividedStr(path, '.')
        valueByKey: object = self.__configs.get(key)
        currentPath: str = path.replace('{key}.'.format(key=key), '')
        return self.__getNestedValueByPath(currentPath, valueByKey)

    def __getNestedValueByPath(self, path: str, value: object) -> object:
        key: str = StrUtil.getFirstStrFromDividedStr(path, '.')
        if key == path:
            return value.get(key)
        valueByKey: object = value.get(key)
        if not DataUtil.isDict(valueByKey):
            raise Exception('Given path is not valid.')
        currentPath: str = path.replace('{key}.'.format(key=key), '')
        return self.__getNestedValueByPath(currentPath, valueByKey)
