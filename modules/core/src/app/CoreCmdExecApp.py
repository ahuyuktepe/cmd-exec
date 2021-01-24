from src.app.CmdExecApp import CmdExecApp
from src.context.AppContextManager import AppContextManager
from src.service.CommandService import CommandService


class CoreCmdExecApp(CmdExecApp):
    __cmdService: CommandService

    def __init__(self, context: AppContextManager):
        super().__init__(context)
        self.__cmdService = context.getService('cmdService')

    def run(self):
        print('Running application via CoreCmdExecApp')
        cid = self._args.getCmd()
        print('cid: ' + cid)
        cmd = self.__cmdService.buildCmdFromId(cid)
        cmd.print()
