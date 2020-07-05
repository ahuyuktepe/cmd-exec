from classes.utils.StrUtil import StrUtil


class AppConfigPath:
    __path: str
    __names: list
    __index: int

    def __init__(self, path: str):
        if not isinstance(path, str) or StrUtil.isNoneOrEmpty(path):
            self.__names = []
        self.__names = path.split('.')
        self.__index = 0

    def nextName(self):
        self.__index = self.__index + 1

    def getCurrentName(self) -> str:
        return self.__names[self.__index]

    def hasNextName(self) -> bool:
        return (self.__index + 1) < len(self.__names)
