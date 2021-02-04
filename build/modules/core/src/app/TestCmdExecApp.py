from src.app.CmdExecApp import CmdExecApp
from src.context.AppContextManager import AppContextManager
from src.service.CommandService import CommandService


class TestCmdExecApp(CmdExecApp):
    __cmdService: CommandService

    def __init__(self, context: AppContextManager):
        super().__init__(context)
        self.__cmdService = context.getService('cmdService')

    def run(self):
        print('TestCmdExecApp is running.')
