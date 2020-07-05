
class DataUtil:
    @staticmethod
    def isInt(value: object):
        return value is not None and (isinstance(value, int) or str(value).isnumeric())
