import json
import os
import xml.etree.ElementTree as ET

from app_runner.enums.UIColor import UIColor
from app_runner.errors.AppRunnerError import AppRunnerError
from _elementtree import Element


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
            raise AppRunnerError("Json content is not valid.")

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
        idCount = len(arr)
        if idCount == 3:
            return {
                'module': arr[0],
                'class': arr[1],
                'method': arr[2]
            }
        elif idCount == 2:
            return {
                'module': arr[0],
                'class': arr[1],
                'method': defaultMethod
            }
        else:
            raise Exception('Given class path is invalid.')

    @staticmethod
    def prependModule(path: str, module: str) -> str:
        if not StrUtil.isNoneOrEmpty(path):
            arr: list = path.split('.')
            idCount = len(arr)
            if idCount < 3:
                return module + '.' + path
            else:
                return path
        else:
            return None

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
    def getFilePropertiesFromStr(sid: str) -> dict:
        arr: list = sid.split('.')
        props: dict = {'module': None, 'file': None}
        if len(arr) > 1:
            props['module'] = arr[0]
            props['file'] = arr[1]
        elif len(arr) == 1:
            props['file'] = arr[0]
        return props

    @staticmethod
    def getAlignedAndLimitedStr(text: str, limit: int, align: str) -> str:
        retStr = text[0:limit]
        if align == 'center':
            return ('{:^' + str(limit) + '.' + str(limit-1) + '}').format(retStr)
        elif align == 'left':
            return ('{:<' + str(limit) + '.' + str(limit-1) + '}').format(retStr)
        elif align == 'right':
            return ('{:>' + str(limit) + '.' + str(limit-1) + '}').format(retStr)
        return retStr

    @staticmethod
    def buildObjFromXmlStr(xmlStr: str) -> Element:
        return ET.fromstring(xmlStr)

    @staticmethod
    def splitStrIntoChunks(srcStr: str, chrCountPerChunk: int):
        return [srcStr[i:i + chrCountPerChunk] for i in range(0, len(srcStr), chrCountPerChunk)]
