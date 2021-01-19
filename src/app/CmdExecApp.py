from src.context.AppContextManager import AppContextManager


class CmdExecApp:
    _contextManager: AppContextManager

    def __init__(self, contextManager: AppContextManager):
        self._contextManager = contextManager

    def run(self):
        pass
