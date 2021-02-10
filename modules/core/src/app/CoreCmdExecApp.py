from src.app.CmdExecApp import CmdExecApp
from src.context.AppContextManager import AppContextManager
from src.service.CommandService import CommandService
from src.service.FieldService import FieldService


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
        print('Passed command id: ' + str(cid))
        # 2) Build command object
        cmd = self.__cmdService.buildCmdFromId(cid)
        cmd.print()
        # 3) Get field values from command params and merge
        values: dict = self.__fieldService.getFieldValuesFromArgumentFile(cmd)
        cmd.setValues(values)
        # 4) Get arguments from command params and merge
        if cmd.hasRequiredFieldWithoutValue():
            values = self.__fieldService.getFieldValuesFromCmdArgs(cmd)
            cmd.setValues(values)
        # 5) Get arguments
        if cmd.hasRequiredFieldWithoutValue():
            values = self.__fieldService.getFieldValuesFromUser(cmd)
            cmd.setValues(values)
        # 4) Execute command
        self.__cmdService.execute(cmd)
