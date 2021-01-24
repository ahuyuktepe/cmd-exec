from src.command.CmdExecutor import CmdExecutor
from src.command.Field import Field


class Command:
    __id: str
    __title: str
    __executor: CmdExecutor
    __method: str
    __fields: list

    def __init__(self, cid: str, title: str):
        self.__id = cid
        self.__title = title
        self.__fields = []
        self.__method = None
        self.__executor = None

    # Setter Methods

    def setExecutor(self, executor: CmdExecutor):
        self.__executor = executor

    def setMethod(self, method: str):
        self.__method = method

    def addField(self, field: Field):
        self.__fields.append(field)

    # Utility Methods

    def execute(self):
        pass

    def print(self):
        print('id: ' + self.__id + ' | title: ' + self.__title)
        self.__executor.print()
