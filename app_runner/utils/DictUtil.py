
class DictUtil:

    @staticmethod
    def hasTrueValue(srcDict: dict, key: str) -> bool:
        value = srcDict.get(key)
        if value == 'true':
            return True
        return False

    @staticmethod
    def getDefaultIntValueIfNone(srcDict: dict, key: str, defVal: int) -> int:
        value = srcDict.get(key)
        if value is None:
            return defVal
        return int(value)

    @staticmethod
    def getDefaultStrValueIfNone(srcDict: dict, key: str, defVal: str) -> str:
        value = srcDict.get(key)
        if value is None:
            return defVal
        return str(value)

