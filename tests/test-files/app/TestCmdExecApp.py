from src.app.CmdExecApp import CmdExecApp
from src.context.AppContextManager import AppContextManager


class TestCmdExecApp(CmdExecApp):

    def __init__(self, context: AppContextManager):
        super().__init__(context)

    def run(self):
        print('TestCmdExecApp is running.')
