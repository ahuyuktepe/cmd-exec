
class DataUtil:
    @staticmethod
    def isInt(value: object):
        return value is not None and (isinstance(value, int) or str(value).isnumeric())

    @staticmethod
    def getDefaultIfNone(value: object, defaultValue: object) -> object:
        if value is None:
            return defaultValue
        return value

    @staticmethod
    def isNullOrEmpty(val: dict):
        return not bool(val)
