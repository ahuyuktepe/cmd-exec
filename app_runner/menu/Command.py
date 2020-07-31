from app_runner.field.Field import Field

class Command:
    _id: str = None
    _description: str = None
    _executor: str = None
    _fields: dict = {}
    _module: str

    def __init__(self, id: str, description: str, executor: str, module: str):
        self._id = id
        self._description = description
        self._executor = executor
        self._module = module

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

    def print(self):
        strVal = "id: {id}\ndescription: {description}\nexecutor: {executor}".format(
            id=self._id,
            description=self._description,
            executor=self._executor
        )
        for id, field in self._fields.items():
            strVal += '\n' + (field.toString())
        print(strVal)
