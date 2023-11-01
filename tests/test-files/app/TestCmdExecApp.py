from cmd_exec.app.CmdExecApp import CmdExecApp
from cmd_exec.context.AppContextManager import AppContextManager
from cmd_exec.menu.Command import Command


class TestCmdExecApp(CmdExecApp):

    def __init__(self, context: AppContextManager):
        super().__init__(context)

    def run(self, cmd: Command, cid: str):
        print('TestCmdExecApp is running.')
