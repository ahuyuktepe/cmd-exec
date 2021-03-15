from src.command.CmdExecutor import CmdExecutor


class Command:
    _id: str
    _title: str
    _executor: CmdExecutor
    _fields: dict
    _module: str

    def __init__(self, cid: str, title: str, module: str):
        self._id = cid
        self._title = title
        self._fields = {}
        self._executor = None
        self._module = module

    def setExecutor(self, executor: CmdExecutor):
        self._executor = executor

    def setFields(self, fields: list):
        if fields is not None and isinstance(fields, list):
            for field in fields:
                self._fields[field.getId()] = field

    def setValues(self, values: dict):
        if values is not None and isinstance(values, dict):
            for fid, field in self._fields.items():
                value = values.get(fid)
                field.setValue(value)

    def getId(self) -> str:
        return self._id

    def getExecutor(self) -> CmdExecutor:
        return self._executor

    def getFields(self) -> dict:
        return self._fields

    def getFieldIds(self) -> list:
        return list(self._fields.keys())

    def getModule(self) -> str:
        return self._module

    def print(self):
        print('id: ' + self._id + ' | title: ' + self._title)
