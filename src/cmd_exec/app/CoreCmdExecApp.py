from ..app.CmdExecApp import CmdExecApp
from ..context.AppContextManager import AppContextManager
from ..menu.Command import Command
from ..service.CommandService import CommandService
from ..service.ConfigurationService import ConfigurationService
from ..service.FieldService import FieldService
from ..util.SystemUtil import SystemUtil


class CoreCmdExecApp(CmdExecApp):
    __cmdService: CommandService
    __fieldService: FieldService

    def __init__(self, context: AppContextManager):
        super().__init__(context)
        self.__cmdService = context.getService('cmdService')
        self.__fieldService = context.getService('fieldService')

    def run(self):
        # 1) Get command id
        cid = self._args.getCmd()
        # 2) Build command object
        cmd: Command = self.__cmdService.buildCmdFromId(cid)
        # 3) Validate User Permission
        uname = SystemUtil.getCurrentUserName()
        cmd.validateUserPermission(uname)
        # 4) Validate User Group Permission
        if not SystemUtil.isWindows():
            groupNames: list = SystemUtil.getCurrentUserGroups()
            cmd.validateUserGroupPermission(uname, groupNames)
        # 5) Get field values from command params and merge
        values: dict = self.__fieldService.getFieldValuesFromArgumentFile(cmd)
        # 6) Get arguments from command params and merge
        valuesFromCmd: dict = self.__fieldService.getFieldValuesFromCmdArgs(cmd)
        for key, value in valuesFromCmd.items():
            if value is not None:
                values[key] = value
        cmd.setValues(values)
        # 7) Run command
        cmd.execute()
