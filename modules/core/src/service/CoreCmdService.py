from src.command.CmdExecutor import CmdExecutor
from src.menu.Command import Command
from src.service.ArgumentService import ArgumentService
from src.service.CommandService import CommandService
from src.service.FieldService import FieldService
from src.util.ModuleUtil import ModuleUtil
from src.util.ObjUtil import ObjUtil
from src.util.ValidationUtil import ValidationUtil


class CoreCmdService(CommandService):
    __fieldService: FieldService
    __argService: ArgumentService

    def __init__(self, fieldService: FieldService, argService: ArgumentService):
        self.__fieldService = fieldService
        self.__argService = argService

    def execute(self, cmd: Command):
        self.__validateFields(cmd)
        cmd.execute()
        pass

    def __validateFields(self, cmd: Command):
        pass

    def buildCmdFromId(self, cid: str) -> Command:
        props = ModuleUtil.getModuleCommandProps(cid)
        # Init Command Object
        cmd: Command = self.__getCommand(cid, props)
        # Init Executor Object
        executor: CmdExecutor = self.__getExecutor(cid, props)
        cmd.setExecutor(executor)
        # Get Fields
        fieldProps = props.get('fields')
        if fieldProps is not None:
            fields = self.__getFields(cid, fieldProps)
            cmd.setFields(fields)
        return cmd

    def __getFields(self, cid: str, fields: list) -> list:
        ValidationUtil.failIfNotType(fields, list, 'ERR45')
        retList = []
        for fieldProps in fields:
            field = self.__fieldService.buildField(cid, fieldProps)
            retList.append(field)
        return retList

    def __getExecutor(self, cid: str, props: dict) -> CmdExecutor:
        # Set Executor
        execProps: dict = props.get('executor')
        ValidationUtil.failIfNotType(execProps, dict, 'ERR37', {'cid': cid})
        cls = execProps.get('class')
        ValidationUtil.failIfStrNoneOrEmpty(cls, 'ERR38', {'cid': cid})
        path = 'modules.{module}.src.executor.{cls}'.format(module=props.get('module'), cls=cls)
        ValidationUtil.failIfClassFileDoesNotExist(path, 'ERR51', {'path': path})
        method = execProps.get('method')
        if method is not None:
            ValidationUtil.failIfNotType(method, str, 'ERR39', {'cid': cid})
        executor = ObjUtil.initClassFromStr(path, cls, [method])
        ValidationUtil.failIfNotType(executor, CmdExecutor, 'ERR40', {'cid': cid})
        executor.setContextManager(self._contextManager)
        return executor

    def __getCommand(self, cid: str, props: dict) -> Command:
        cmdId = props.get('id')
        ValidationUtil.failIfStrNoneOrEmpty(cmdId, 'ERR35', {'cid': cid})
        title = props.get('title')
        ValidationUtil.failIfStrNoneOrEmpty(title, 'ERR36', {'cid': cid})
        mid = props.get('module')
        ValidationUtil.failIfStrNoneOrEmpty(mid, 'ERR41', {'cid': cid})
        return Command(props.get('id'), props.get('title'))
