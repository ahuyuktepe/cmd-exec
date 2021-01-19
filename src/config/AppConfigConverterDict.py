from src.util.ValidationUtil import ValidationUtil


class AppConfigConverterDict:
    # Static Variables
    __pathValueDict: dict = {}
    __keys: list = []
    # Instance Variables
    __currentValue: object
    __currentKey: str

    def __init__(self):
        self.__currentValue = None
        self.__pathValueDict = {}
        self.__currentKey = None

    # Setter Methods

    def addKey(self, key: str):
        self.__keys.append(key)

    def removeLastKey(self):
        if len(self.__keys) > 0:
            self.__keys.pop()

    def setCurrentValue(self, newValue: object):
        self.__currentValue = newValue

    def setCurrentKey(self, key: str):
        self.__currentKey = key

    def savePathAndValue(self):
        path = ".".join(self.__keys)
        self.__pathValueDict[path] = self.__currentValue

    def reset(self):
        self.__currentValue = None
        self.__currentKey = None
        self.__keys.clear()
        self.__pathValueDict.clear()

    # Getter Methods

    def getCurrentValue(self) -> object:
        return self.__currentValue

    def getPathValueDict(self) -> dict:
        return self.__pathValueDict

    def hasNext(self) -> bool:
        if self.__currentKey is None:
            return True
        elif not isinstance(self.__currentValue, dict):
            return False
        return True
