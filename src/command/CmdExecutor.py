from src.context.AppContextManager import AppContextManager
from src.field.FieldValues import FieldValues


class CmdExecutor:
    _contextManager: AppContextManager
    _method: str

    def __init__(self, method: str):
        self._method = method

    # Setter Methods

    def setContextManager(self, contextManager: AppContextManager):
        self._contextManager = contextManager

    # Getter Methods

    def getMethod(self) -> str:
        return self._method

    def hasCustomMethod(self) -> bool:
        return self._method is not None

    # Utility Method

    def execute(self, values: FieldValues):
        pass

    def print(self):
        print('cls: ' + self._cls + ' | method: ' + str(self._method))
