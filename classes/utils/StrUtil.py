from classes.utils.ListUtil import ListUtil


class StrUtil:

    @staticmethod
    def isStr(value: object) -> bool:
        return isinstance(value, str)

    @staticmethod
    def isNoneOrNotString(value: object):
        return value is None or not StrUtil.isStr(value)

    @staticmethod
    def getFirstStrFromDividedStr(sourceStr: str, divider: str) -> str:
        if sourceStr is None:
            return None
        dividerIndex: int = sourceStr.find(divider)
        if dividerIndex == -1:
            return sourceStr
        return sourceStr[0:dividerIndex]

    @staticmethod
    def strToInt(value: str):
        if not value.isnumeric():
            raise Exception('Given string is not numeric')
        return int(value)
