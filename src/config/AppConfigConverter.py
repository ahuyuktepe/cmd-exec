from src.config.AppConfigConverterDict import AppConfigConverterDict


class AppConfigConverter:
    __values: AppConfigConverterDict

    def __init__(self):
        self.__values = AppConfigConverterDict()

    def convert(self, srcDict: dict) -> dict:
        self.reset()
        self.__values.setCurrentValue(srcDict)
        self.__convert(self.__values)
        return self.__values.getPathValueDict()

    def reset(self):
        self.__values.reset()

    def __convert(self, srcDict: AppConfigConverterDict):
        if not srcDict.hasNext():
            srcDict.savePathAndValue()
        else:
            for key, value in srcDict.getCurrentValue().items():
                srcDict.setCurrentKey(key)
                srcDict.addKey(key)
                srcDict.setCurrentValue(value)
                self.__convert(srcDict)
        srcDict.removeLastKey()
