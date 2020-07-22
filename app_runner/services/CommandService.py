from app_runner.menu.Command import Command
from app_runner.services.BaseService import BaseService
from app_runner.utils.ErrorUtil import ErrorUtil
from app_runner.utils.ObjUtil import ObjUtil

class CommandService(BaseService):

    def getCommands(self, cmdObjects: list) -> dict:
        ErrorUtil.raiseExceptionIfNone(cmdObjects)
        commands: dict = {}
        if commands is not None:
            for cmdObj in cmdObjects:
                commands[cmdObj.get('id')] = self.buildCmd(cmdObj)
        return commands

    def buildCmd(self, cmdProps: dict) -> Command:
        ErrorUtil.raiseExceptionIfNone(cmdProps)
        # self.log('debug', 'Building command {id}', {"id": cmdProps.get('id')})
        cmd: Command = Command(
            id=cmdProps.get('id'),
            description=cmdProps.get('description'),
            executor=cmdProps.get('executor')
        )
        return cmd

    def initializeExecutorClass(self, className: str) -> object:
        ErrorUtil.raiseExceptionIfNone(className)
        cls = ObjUtil.getClassFromStr('executors', className)
        return cls()

    def callExecutorMethod(self, executor: object, methodName: str, values: dict):
        ErrorUtil.raiseExceptionIfNone(methodName)
        method: object = getattr(executor, methodName)
        method(values)

    def getValuesWithDefaultValues(self, values: dict, cmd: Command) -> dict:
        retDict: dict = {}
        for fid, field in cmd.getFields().items():
            retDict[fid] = field.getDefaultValueIfNone(values.get(fid))
        return retDict
