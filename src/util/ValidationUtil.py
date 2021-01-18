import os
from src.error.CmdExecError import CmdExecError
from src.util.FileUtil import FileUtil


class ValidationUtil:

    @staticmethod
    def failIfDirectoryCanNotBeAccessed(path: list, code: str, params: dict = {}):
        if not FileUtil.isDirectoryReadable(path):
            raise CmdExecError(code, params)

    @staticmethod
    def failIfFileCanNotBeAccessed(path: list, code: str, params: dict = {}):
        if not FileUtil.isFileReadable(path):
            raise CmdExecError(code, params)

    @staticmethod
    def failIfEnvironmentVarIsNotValid(name: str):
        if name not in os.environ:
            raise CmdExecError('ERR04', {'name': name})
        value = os.environ[name]
        if value in [None, '', '/']:
            raise CmdExecError('ERR04', {'name': name})

    @staticmethod
    def failIfStrNoneOrEmpty(val: str, code: str, params: dict = {}):
        if val is None or val == '':
            raise CmdExecError(code, params)

    # ==================================================================================================================
    # @staticmethod
    # def failIfStringContainsChars(srcStr: str, chars: list, code: str, params: dict={}):
    #     for char in chars:
    #         if char in srcStr:
    #             raise CmdExecError(code, params)
