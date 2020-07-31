from app_runner.errors.FieldValidationError import FieldValidationError
from app_runner.utils.DataUtil import DataUtil
from app_runner.utils.ErrorUtil import ErrorUtil

class Field:
    _id: str
    _type: str
    _label: str
    _required: bool
    _validator: str
    _default: object

    def __init__(self, properties: dict):
        ErrorUtil.raiseExceptionIfNone(properties, "Field 'properties' is None.")
        ErrorUtil.raiseExceptionIfNone(properties.get('id'), "Field 'id' is None.")
        ErrorUtil.raiseExceptionIfNone(properties.get('label'), "Field 'label' is None.")
        self._id = properties.get('id')
        self._type = properties.get('type')
        self._label = properties.get('label')
        self._required = DataUtil.getDefaultIfNone(properties.get('required'), False)
        self._validator = properties.get('validator')
        self._default = properties.get('default')

    def toString(self) -> str:
        return "id: {id}, type: {type}, label: {label}, isRequired: {required}, validator: {validator}".format(
            id=self._id,
            label=self._label,
            type=self._type,
            required=self._required,
            validator=self._validator
        )

    def isRequired(self) -> bool:
        return self._required

    def getId(self) -> str:
        return self._id

    def getLabel(self) -> str:
        return self._label

    def getDefault(self) -> object:
        return self._default

    def getType(self) -> str:
        return self._type

    def getValidator(self) -> dict:
        return self._validator

    def validate(self, value: object):
        if self.isRequired() and value is None:
            raise FieldValidationError("Field '" + self._id + "' is required but has no value.")

    def isNumber(self) -> bool:
        return self._type == 'number'

    def isText(self) -> bool:
        return self._type == 'text'

    def isDate(self) -> bool:
        return self._type == 'date'

    def isDateTime(self) -> bool:
        return self._type == 'datetime'

    def hasCustomValidator(self) -> bool:
        return self._validator is not None

    def hasOptions(self) -> bool:
        return False

    def hasDefaultValue(self) -> bool:
        return self._default is not None
