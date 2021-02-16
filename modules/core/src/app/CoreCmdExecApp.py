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
        # 5) Execute command
        self.__cmdService.execute(cmd)
