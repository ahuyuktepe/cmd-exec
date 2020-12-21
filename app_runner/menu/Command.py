from app_runner.field.Field import Field

class Command:
    _id: str
    _description: str
    _executor: str
    _fields: dict
    _menus: list

    def __init__(self, id: str, description: str):
        self._id = id
        self._description = description
        self._fields = {}

    # Getter Methods

    def getId(self) -> str:
        return self._id

    def getDescription(self) -> str:
        return self._description

    def getExecutor(self) -> str:
        return self._executor

    def getFields(self) -> dict:
        return self._fields

    def getFieldsAsList(self) -> list:
        retList = []
        for id, field in self._fields.items():
            retList.append(field)
        return retList

    def addField(self, field: Field):
        self._fields[field.getId()] = field

    def getMenus(self) -> list:
        return self._menus

    def hasNextMenus(self) -> bool:
        return self._menus is not None

    def hasFields(self) -> bool:
        return self._fields is None or len(self._fields) > 0

    def hasExecutor(self) -> bool:
        return self._executor is not None

    # Setter Methods

    def setExecutor(self, executor: str):
        self._executor = executor

    def setMenus(self, menus: list):
        self._menus = menus

    def setFields(self, fields: list):
        field: Field
        for field in fields:
            self._fields[field.getId()] = field
