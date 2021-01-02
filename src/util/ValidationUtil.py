import os
from src.error.CmdExecError import CmdExecError
from src.util.FileUtil import FileUtil
from src.util.StrUtil import StrUtil


class ValidationUtil:
    @staticmethod
    def failIfObjNone(obj: object, msg: str, params: dict = {}):
        if obj is None:
            raise CmdExecError(msg.format(**params))

    @staticmethod
    def failIfStrNoneOrEmpty(val: str, msg: str, params: dict = {}):
        if val is None or val == '':
            raise CmdExecError(msg.format(**params))

    @staticmethod
    def failIfEnvironmentVarIsNotSet(name: str):
        if name not in os.environ:
            raise CmdExecError("Environment variable '" + name + "' is not set.")

    @staticmethod
    def failIfFileIsNotReadable(path: str, msg: str, params: dict = {}):
        if not FileUtil.isFileReadable(path):
            raise CmdExecError(msg.format(**params))

    @staticmethod
    def failIfVersionSyntaxInvalid(moduleName: str, version: str):
        if StrUtil.isVersionSyntaxInvalid(version):
            raise CmdExecError("Invalid version '{version}' provided for module '{module}'.".format(
                version=version,
                module=moduleName
            ))
