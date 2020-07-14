from classes.errors.FieldValidationError import FieldValidationError
from classes.utils.DataUtil import DataUtil
from classes.utils.ErrorUtil import ErrorUtil

class Field:
    _id: str
    _type: str
    _label: str
    _required: bool
    _validator: str

    def __init__(self, properties: dict):
        ErrorUtil.raiseExceptionIfNone(properties, "Field 'properties' is None.")
        ErrorUtil.raiseExceptionIfNone(properties.get('id'), "Field 'id' is None.")
        ErrorUtil.raiseExceptionIfNone(properties.get('label'), "Field 'label' is None.")
        self._id = properties.get('id')
        self._type = properties.get('type')
        self._label = properties.get('label')
        self._required = DataUtil.getDefaultIfNone(properties.get('required'), False)
        self._validator = properties.get('validator')

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

    def validate(self, value: object):
        if self.isRequired() and value is None:
            raise FieldValidationError("Field '" + self._id + "' is required but has no value.")
