from cmd_exec.action import CmdActionResponse
from cmd_exec.context.AppContextManager import AppContextManager
from cmd_exec.menu.Command import Command


class CmdAction:
    _context: AppContextManager

    def setContextManager(self, contextManager: AppContextManager):
        self._context = contextManager

    def run(self, cmd: Command) -> CmdActionResponse:
        pass
