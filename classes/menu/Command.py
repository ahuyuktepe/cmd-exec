from classes.field.Field import Field

class Command:
    _id: str = None
    _description: str = None
    _executor: str = None
    _fields: dict = {}

    def __init__(self, id: str, description: str, executor: str):
        self._id = id
        self._description = description
        self._executor = executor

    def getId(self):
        return self._id

    def getExecutorClass(self) -> str:
        arr: list = self._executor.split('.')
        if len(arr) > 0:
            return arr[0]
        return None

    def getExecutorMethod(self) -> str:
        arr: list = self._executor.split('.')
        if len(arr) > 1:
            return arr[1]
        return 'execute'

    def getFields(self) -> dict:
        return self._fields

    def addField(self, field: Field):
        self._fields[field.getId()] = field

    def print(self) -> str:
        for field in self._fields:
            print("test" + field.toString())
