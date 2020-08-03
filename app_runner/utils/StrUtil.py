import json
from app_runner.errors.InvalidJsonStrError import InvalidJsonStrError
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

    @staticmethod
    def getClassMethodMapFromStr(clsPath: str, defaultMethod: str) -> dict:
        arr: list = clsPath.split('.')
        props: dict = {'class': None, 'method': None}
        if len(arr) > 1:
            props['class'] = arr[0]
            props['method'] = arr[1]
        elif len(arr) == 1:
            props['class'] = arr[0]
            props['method'] = defaultMethod
        return props

    @staticmethod
    def getServicePropertiesFromStr(sid: str) -> dict:
        arr: list = sid.split('.')
        props: dict = {'class': None, 'module': None}
        if len(arr) > 1:
            props['module'] = arr[0]
            props['class'] = arr[1]
        elif len(arr) == 1:
            props['class'] = arr[0]
        return props

    @staticmethod
    def getConfigPropertiesFromStr(sid: str) -> dict:
        arr: list = sid.split('.')
        props: dict = {'module': None, 'file': None}
        if len(arr) > 1:
            props['module'] = arr[0]
            props['file'] = arr[1]
        elif len(arr) == 1:
            props['file'] = arr[0]
        return props
