import importlib

from classes.menu.Command import Command
from classes.services.BaseService import BaseService
from classes.services.FieldService import FieldService
from classes.utils.ErrorUtil import ErrorUtil

class CommandService(BaseService):
    __fieldService: FieldService

    def setFieldService(self, fieldService: FieldService):
        self.__fieldService = fieldService

    def executeCommand(self, cmd: Command):
        ErrorUtil.raiseExceptionIfNone(cmd)
        className: str = cmd.getExecutorClass()
        if className is not None:
            methodName: str = cmd.getExecutorMethod()
            module = importlib.import_module('executors.{className}'.format(className=className))
            cls = getattr(module, className)
            obj: object = cls()
            method: object = getattr(obj, methodName)
            method()

    def getCommands(self, cmdObjects: list) -> dict:
        ErrorUtil.raiseExceptionIfNone(cmdObjects)
        commands: dict = {}
        if commands is not None:
            for cmdObj in cmdObjects:
                commands[cmdObj.get('id')] = self.buildCmd(cmdObj)
        return commands

    def buildCmd(self, cmdProps: dict) -> Command:
        ErrorUtil.raiseExceptionIfNone(cmdProps)
        self._logService.debug('Building command {id}'.format(id=cmdProps.get('id')))
        cmd: Command = Command(
            id=cmdProps.get('id'),
            description=cmdProps.get('description'),
            executor=cmdProps.get('executor')
        )
        self.__fieldService.insertFields(cmd, cmdProps.get('fields'))
        return cmd
