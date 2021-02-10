from src.command.CmdExecutor import CmdExecutor


class Command:
    _id: str
    _title: str
    _executor: CmdExecutor
    _fields: dict

    def __init__(self, cid: str, title: str):
        self._id = cid
        self._title = title
        self._fields = {}
        self._method = None
        self._executor = None

    # Setter Methods

    def setExecutor(self, executor: CmdExecutor):
        self._executor = executor

    def setMethod(self, method: str):
        self._method = method

    def setFields(self, fields: list):
        if fields is not None and isinstance(fields, list):
            for field in fields:
                self._fields[field.getId()] = field

    def setValues(self, values: dict):
        if values is not None and isinstance(values, dict):
            for fid, field in self._fields.items():
                value = values.get(fid)
                if value is not None:
                    field.setValue(value)

    def hasRequiredFieldWithoutValue(self) -> bool:
        for fid, field in self._fields.items():
            if field.isRequiredAndHaveNoValue():
                return True
        return False

    # Getter Methods

    def getRequiredFieldIdsWithoutValue(self) -> list:
        ids: list = []
        for fid, field in self._fields.items():
            if field.isRequiredAndHaveNoValue():
                ids.append(field.getId())
        return ids

    def getId(self) -> str:
        return self._id

    # Utility Methods

    def execute(self):
        method = getattr(self._executor, self._executor.getMethod())
        method(self._fields)

    def print(self):
        print('id: ' + self._id + ' | title: ' + self._title)
