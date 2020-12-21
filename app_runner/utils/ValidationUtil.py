import os
from app_runner.errors.AppRunnerError import AppRunnerError
from app_runner.menu.Command import Command
from app_runner.utils.FileUtil import FileUtil


class ValidationUtil:

    @staticmethod
    def failIfNotInstanceOf(obj: object, instanceOf, msg: str):
        if not isinstance(obj, instanceOf):
            raise AppRunnerError(msg)

    @staticmethod
    def failIfObjNone(obj: object, msg: str):
        if obj is None:
            raise AppRunnerError(msg)

    @staticmethod
    def failIfEnvironmentVarIsNotSet(name: str):
        if name not in os.environ:
            raise AppRunnerError("Environment variable '" + name + "' is not set.")

    @staticmethod
    def failIfFileIsNotReadable(path: str, msg: str):
        if not FileUtil.isFileReadable(path):
            raise AppRunnerError(msg)

    @staticmethod
    def failIfDoesNotFit(parentSize: int, childSize: int, msg: str):
        if childSize > parentSize:
            raise AppRunnerError(msg)

    @staticmethod
    def failIfClassMethodDoesNotExist(obj: object, classPath: str, methodName: str):
        if not hasattr(obj, methodName):
            raise AppRunnerError("Class '" + classPath + "' does not have method '" + methodName + "'")

    @staticmethod
    def failIfCommandIsNone(cmd: Command):
        if cmd is None:
            raise AppRunnerError("Given command object is None.")

    @staticmethod
    def failIfDerivedAreaWidthDoesNotFit(derivedWidth: int, parentAreaWidth: int):
        if derivedWidth > parentAreaWidth:
            raise AppRunnerError("Derived print area does not fit.")
