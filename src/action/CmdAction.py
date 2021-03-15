from src.action import CmdActionResponse
from src.context.AppContextManager import AppContextManager
from src.menu.Command import Command


class CmdAction:
    _context: AppContextManager

    def setContextManager(self, contextManager: AppContextManager):
        self._context = contextManager

    def run(self, cmd: Command) -> CmdActionResponse:
        pass
