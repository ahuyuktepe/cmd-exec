import json
from classes.errors.InvalidJsonStrError import InvalidJsonStrError

class StrUtil:

    @staticmethod
    def strToInt(value: str) -> int:
        if not value.isnumeric():
            raise Exception('Given string is not numeric')
        return int(value)

    @staticmethod
    def jsonStrToObj(jsonStr: str) -> object:
        try:
            return json.loads(jsonStr)
        except ValueError:
            raise InvalidJsonStrError()

    @staticmethod
    def isNoneOrEmpty(value: str):
        return value is None or value == ''
