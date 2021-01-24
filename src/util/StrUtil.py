import importlib
import os

from src.error.CmdExecError import CmdExecError


class StrUtil:
    @staticmethod
    def getCommandPropertiesFromStr(cid: str) -> dict:
        arr: list = cid.split('.')
        props: dict = {'module': 'core', 'cid': None}
        if len(arr) > 1:
            props['module'] = arr[0]
            props['cid'] = arr[1]
        elif len(arr) == 1:
            props['cid'] = arr[0]
        return props

    @staticmethod
    def getFilePropertiesFromStr(sid: str) -> dict:
        arr: list = sid.split('.')
        props: dict = {'module': 'core', 'file': None}
        if len(arr) > 1:
            props['module'] = arr[0]
            props['file'] = arr[1]
        elif len(arr) == 1:
            props['file'] = arr[0]
        return props

    @staticmethod
    def getClassMethodMapFromStr(clsPath: str, defaultMethod: str = None) -> dict:
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
    def getModuleServiceMapFromStr(servicePath: str) -> dict:
        arr: list = servicePath.split('.')
        count = len(arr)
        if count == 1:
            return {'mid': None, 'sid': servicePath}
        elif count == 2:
            return {'mid': arr[0], 'sid': arr[1]}
        else:
            CmdExecError('ERR25', {'path': servicePath})

    @staticmethod
    def isNoneOrEmpty(value: str):
        return value is None or value == ''

    @staticmethod
    def isVersionSyntaxInvalid(version: str) -> bool:
        if version is None:
            return True
        values = version.split('.')
        for value in values:
            if not value.isnumeric():
                return True
        return False

    @staticmethod
    def prefillVersion(version: str, fillCount: int = 2) -> str:
        arr = []
        if version is not None:
            values = version.split('.')
            for value in values:
                arr.append(value.zfill(fillCount))
        return '.'.join(arr)

    @staticmethod
    def convertClassPathToFilePath(clsPath: str) -> list:
        if isinstance(clsPath, str) and not StrUtil.isNoneOrEmpty(clsPath):
            return clsPath.split('.')

    @staticmethod
    def convertClassNameStrToClass(clsPath: str, clsName: str):
        module = importlib.import_module(clsPath)
        cls = getattr(module, clsName)
        return cls
