from src.context.AppContextManager import AppContextManager


class CmdExecutor:
    _contextManager: AppContextManager
    _cls: str
    _method: str

    def __init__(self, cls: str):
        self._cls = cls
        self._method = None

    def setMethod(self, method: str):
        self._method = method

    def setContextManager(self, contextManager: AppContextManager):
        self._contextManager = contextManager

    def execute(self):
        pass

    def print(self):
        print('cls: ' + self._cls + ' | method: ' + str(self._method))
