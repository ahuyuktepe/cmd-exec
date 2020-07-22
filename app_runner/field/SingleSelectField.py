from app_runner.errors.FieldValidationError import FieldValidationError
from app_runner.field.Field import Field
from app_runner.utils.ListUtil import ListUtil
from app_runner.utils.ObjUtil import ObjUtil


class SingleSelectField(Field):
    _options: list
    _optionGetter: str

    def __init__(self, properties: dict):
        super().__init__(properties)

    def populateOptions(self, optionGetter: str, options: list):
        if optionGetter is not None:
            getterClass = ObjUtil.getClassFromStr('getters', optionGetter)
            self.setOptions(getterClass().getOptions(self))
        else:
            self.setOptions(options)

    def setOptions(self, options: list):
        self._options = options

    def getOptions(self) -> list:
        return self._options

    def hasOptionGetter(self) -> bool:
        return self._optionGetter is not None

    def validate(self, value: object):
        super().validate(value)
        valStr: str = str(value)
        if not ListUtil.hasElementByKey(self._options, 'id', valStr):
            raise FieldValidationError("Field '" + self._id + "' value '" + valStr + "' is not in options.")
