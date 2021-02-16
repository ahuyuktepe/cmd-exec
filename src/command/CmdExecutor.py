from src.context.AppContextManager import AppContextManager
from src.util.StrUtil import StrUtil


class CmdExecutor:
    _contextManager: AppContextManager
    _method: str

    def __init__(self, method: str):
        if StrUtil.isNoneOrEmpty(method):
            self._method = "execute"
        else:
            self._method = method

    def setContextManager(self, contextManager: AppContextManager):
        self._contextManager = contextManager

    def getMethod(self) -> str:
        return self._method

    def execute(self, fields: dict):
        pass

    def print(self):
        print('method: ' + str(self._method))
