import os
from src.errors.CmdExecError import CmdExecError


class ValidationUtil:
    @staticmethod
    def failIfObjNone(obj: object, msg: str):
        if obj is None:
            raise CmdExecError(msg)

    @staticmethod
    def failIfEnvironmentVarIsNotSet(name: str):
        if name not in os.environ:
            raise CmdExecError("Environment variable '" + name + "' is not set.")
