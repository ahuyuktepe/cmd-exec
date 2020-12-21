from app_runner.errors.FieldValidationError import FieldValidationError
from app_runner.errors.FieldValidationErrors import FieldValidationErrors
from app_runner.field.Field import Field
from app_runner.utils.ListUtil import ListUtil
from app_runner.utils.StrUtil import StrUtil


class MultiSelectField(Field):
    _options: list
    _optionGetter: str

    def __init__(self, properties: dict):
        super().__init__(properties)

    # Getter Methods

    def getOptions(self) -> list:
        return self._options

    def getOptionGetter(self) -> str:
        return self._optionGetter

    # Setter Methods

    def setOptionGetter(self, mid: str, getter: str):
        getterPath = None
        if getter is not None:
            getterPath = StrUtil.prependModule(getter, mid)
        self._optionGetter = getterPath

    def setOptions(self, options: list):
        self._options = options

    # Query Methods

    def hasOptionGetter(self) -> bool:
        return self._optionGetter is not None

    def hasOptions(self) -> bool:
        return True

    # Utility Methods

    def validate(self, value: object, errors: FieldValidationErrors):
        super().validate(value, errors)
        if self.isRequired() and len(value) == 0:
            errors.addError(FieldValidationError("Please select an option.", self.getId()))
        elif len(value) > 0:
            for currentVal in value:
                if not ListUtil.hasElementByKey(self._options, 'id', currentVal):
                    errors.addError(FieldValidationError("Field '" + self._id + "' value '" + currentVal + "' is not in options.", self.getId()))
