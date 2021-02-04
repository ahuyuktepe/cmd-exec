from src.command.CmdExecutor import CmdExecutor
from src.field.Field import Field
from src.field.FieldValues import FieldValues


class Command:
    _id: str
    _title: str
    _executor: CmdExecutor
    _fields: list

    def __init__(self, cid: str, title: str):
        self._id = cid
        self._title = title
        self._fields = []
        self._method = None
        self._executor = None

    # Setter Methods

    def setExecutor(self, executor: CmdExecutor):
        self._executor = executor

    def setMethod(self, method: str):
        self._method = method

    def setFields(self, fields: list):
        self._fields = fields

    def addField(self, field: Field):
        self._fields.append(field)

    # Utility Methods

    def execute(self, values: FieldValues):
        if self._executor.hasCustomMethod():
            method = getattr(self._executor, self._executor.getMethod())
            method(values)
        else:
            self._executor.execute(values)

    def print(self):
        print('id: ' + self._id + ' | title: ' + self._title)
