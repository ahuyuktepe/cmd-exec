from classes.errors.FieldValidationError import FieldValidationError
from classes.field.Field import Field

class TextField(Field):
    _minSize: int
    _maxSize: int

    def __init__(self, properties: dict):
        super().__init__(properties)
        self._minSize = properties.get('min_size')
        self._maxSize = properties.get('max_size')

    def validate(self, value: object):
        super().validate(value)
        valueStr = str(value)
        if self._maxSize is not None and self._maxSize < len(valueStr):
            raise FieldValidationError("Field '" + self._id + "' is assigned to string '" + valueStr + "' with size greater than max size '" + str(self._maxSize) + "'.")
        if self._minSize is not None and self._minSize > len(valueStr):
            raise FieldValidationError("Field '" + self._id + "' is assigned to string '" + valueStr + "' with size less than min size '" + str(self._minSize) + "'.")
