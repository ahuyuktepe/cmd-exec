import json
from classes.errors.InvalidJsonStrError import InvalidJsonStrError
import os

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


    @staticmethod
    def getFileNameFromPath(path: str) -> str:
        divider: str = os.path.sep
        values: list = path.split(divider)
        return values[-1]

    @staticmethod
    def removeFileExtension(fileName: str) -> str:
        values: list = fileName.split('.')
        return values[0]

    @staticmethod
    def getObjFromArgsStr(args: str):
        argsDict: dict = {}
        values: list = args.split(',')
        for value in values:
            arr: list = value.split(':')
            argsDict[arr[0]] = arr[1]
        return argsDict
