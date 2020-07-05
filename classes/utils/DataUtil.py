
class DataUtil:
    @staticmethod
    def isStrOrNumber(self, value: object) -> bool:
        return value is not None and (isinstance(value, str) or isinstance(value, int))

    @staticmethod
    def isDict(value: object) -> bool:
        return isinstance(value, dict)

    @staticmethod
    def isArray(value: object) -> bool:
        return isinstance(value, list)

    @staticmethod
    def isInt(value: object):
        return value is not None and isinstance(value, int)
