from app_runner.errors.CmdExecError import CmdExecError
from app_runner.menu.Command import Command
from app_runner.utils.FileUtil import FileUtil


class ValidationUtil:

    @staticmethod
    def failIfFileNotReadable(filePath: str):
        if FileUtil.isDirectory(filePath):
            raise CmdExecError("File expected but directory given by path '" + filePath + "'.")
        elif not FileUtil.doesFileExist(filePath):
            raise CmdExecError("File '" + filePath + "' does not exist.")
        elif not FileUtil.doesUserHaveAccessOnFile(filePath):
            raise CmdExecError("Executing user does not have read access on file '" + filePath + "'.")
    @staticmethod
    def validateCmdProps(props: dict):
        if props is None:
            raise CmdExecError('Given command properties object is null.')
        elif props.get('executor') is None:
            raise CmdExecError("Command '" + props.get('id') + "' is not assigned to an executor.")

    @staticmethod
    def failIfObjNone(obj: object, msg: str):
        if obj is None:
            raise CmdExecError(msg)

    @staticmethod
    def failIfServiceClassIsNotDefined(mid: str, cls: str):
        if mid is not None:
            filePath: str = FileUtil.getAbsolutePath(['modules', mid, 'src', 'services', cls + '.py'])
            if not FileUtil.doesFileExist(filePath):
                raise CmdExecError("Service class does not exist in given path '" + filePath + "'.")

    @staticmethod
    def failIfClassNotDefined(mid: str, cls: str, dirName: str):
        if mid is not None:
            filePath: str = FileUtil.getAbsolutePath(['modules', mid, 'src', dirName, cls + '.py'])
            if not FileUtil.doesFileExist(filePath):
                raise CmdExecError("Class does not exist in given path '" + filePath + "'.")

    @staticmethod
    def failIfClassMethodDoesNotExist(obj: object, classPath: str, methodName: str):
        if not hasattr(obj, methodName):
            raise CmdExecError("Class '" + classPath + "' does not have method '" + methodName + "'")

    @staticmethod
    def failIfCommandIsNone(cmd: Command):
        if cmd is None:
            raise CmdExecError("Given command object is None.")
