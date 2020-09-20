from app_runner.field.Field import Field

class Command:
    _id: str = None
    _description: str = None
    _executor: str = None
    _fields: dict = {}
    _menu: str

    def __init__(self, id: str, description: str):
        self._id = id
        self._description = description

    # Getter Methods

    def getId(self) -> str:
        return self._id

    def getDescription(self) -> str:
        return self._description

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

    def getModule(self) -> str:
        return self._module

    def addField(self, field: Field):
        self._fields[field.getId()] = field

    def getMenu(self) -> str:
        return self._menu

    def hasNextMenu(self) -> bool:
        return self._menu is not None

    # Setter Methods

    def setExecutor(self, executor: str):
        self._executor = executor

    def setMenu(self, menu: str):
        self._menu = menu

    def setFields(self, fields: list):
        field: Field
        for field in fields:
            self._fields[field.getId()] = field

    def print(self):
        strVal = "id: {id}\ndescription: {description}\nexecutor: {executor}".format(
            id=self._id,
            description=self._description,
            executor=self._executor
        )
        for id, field in self._fields.items():
            strVal += '\n' + (field.toString())
        print(strVal)
