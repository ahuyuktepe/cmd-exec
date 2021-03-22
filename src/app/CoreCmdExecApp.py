from src.action.CmdAction import CmdAction
from src.action.CmdActionResponse import CmdActionResponse
from src.app.CmdExecApp import CmdExecApp
from src.context.AppContextManager import AppContextManager
from src.error.CmdExecError import CmdExecError
from src.menu.Command import Command
from src.service.CommandService import CommandService
from src.service.ConfigurationService import ConfigurationService
from src.service.FieldService import FieldService
from src.util.ObjUtil import ObjUtil
from src.util.ValidationUtil import ValidationUtil


class CoreCmdExecApp(CmdExecApp):
    __cmdService: CommandService
    __fieldService: FieldService
    __configService: ConfigurationService

    def __init__(self, context: AppContextManager):
        super().__init__(context)
        self.__cmdService = context.getService('cmdService')
        self.__fieldService = context.getService('fieldService')
        self.__configService = context.getService('configService')

    def run(self):
        # 1) Get command id
        cid = self._args.getCmd()
        # 2) Build command object
        cmd = self.__cmdService.buildCmdFromId(cid)
        # 3) Get field values from command params and merge
        values: dict = self.__fieldService.getFieldValuesFromArgumentFile(cmd)
        # 4) Get arguments from command params and merge
        valuesFromCmd: dict = self.__fieldService.getFieldValuesFromCmdArgs(cmd)
        for key, value in valuesFromCmd.items():
            if value is not None:
                values[key] = value
        cmd.setValues(values)
        # 5) Handle Before Command Action
        self.__handlePreCommandAction(cmd)
        # 6) Execute command
        self.__cmdService.execute(cmd)
        # 7) Handle After Command Action
        self.__handleAfterCommandAction(cmd)

    def __handlePreCommandAction(self, cmd: Command):
        beforeCmdProps: dict = self.__getBeforeCmdActionPropsByCmd(cmd)
        if beforeCmdProps is not None:
            print('Before Command Props: ' + str(beforeCmdProps))
            cls = beforeCmdProps.get('class')
            ValidationUtil.failIfStrNoneOrEmpty(cls, 'ERR60')
            module = beforeCmdProps.get('module')
            ValidationUtil.failIfStrNoneOrEmpty(module, 'ERR60')
            path = "modules.{module}.src.action.{cls}".format(module=module, cls=cls)
            obj: CmdAction = ObjUtil.initClassFromStr(path, cls)
            ValidationUtil.failIfNotType(obj, CmdAction, 'ERR71')
            obj.setContextManager(self._context)
            response: CmdActionResponse = obj.run(cmd)
            ValidationUtil.failIfNotType(response, CmdActionResponse, 'ERR72', {'path': path})
            if response.isFail():
                raise CmdExecError('ERR73', {'details': response.getMsg()})

    def __handleAfterCommandAction(self, cmd: Command):
        props: dict = self.__getAfterCmdActionPropsByCmd(cmd)
        if props is not None:
            cls = props.get('class')
            ValidationUtil.failIfStrNoneOrEmpty(cls, 'ERR60')
            module = props.get('module')
            ValidationUtil.failIfStrNoneOrEmpty(module, 'ERR60')
            path = "modules.{module}.src.action.{cls}".format(module=module, cls=cls)
            obj: CmdAction = ObjUtil.initClassFromStr(path, cls)
            obj.setContextManager(self._context)
            response: CmdActionResponse = obj.run(cmd)
            ValidationUtil.failIfNotType(response, CmdActionResponse, 'ERR72', {'path': path})
            if response.isFail():
                raise CmdExecError('ERR75', {'details': response.getMsg()})

    def __getBeforeCmdActionPropsByCmd(self, cmd: Command) -> dict:
        actions = self.__configService.getValue('application.actions.before_command')
        if actions is not None:
            ValidationUtil.failIfNotType(actions, list, 'ERR70')
            mid = cmd.getModule()
            cid = cmd.getId()
            return self.__getAction(actions, cid, mid)
        return None

    def __getAfterCmdActionPropsByCmd(self, cmd: Command) -> dict:
        actions = self.__configService.getValue('application.actions.after_command')
        if actions is not None:
            ValidationUtil.failIfNotType(actions, list, 'ERR74')
            mid = cmd.getModule()
            cid = cmd.getId()
            return self.__getAction(actions, cid, mid)
        return None

    def __getAction(self, actions: list, cid: str, mid: str) -> dict:
        for action in actions:
            selector = action.get('selector')
            if selector == '*':
                return action
            elif selector == (mid + '.*'):
                return action
            elif selector == (mid + '.' + cid):
                return action
        return None
