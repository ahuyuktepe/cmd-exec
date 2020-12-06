from app_runner.errors.FieldValidationError import FieldValidationError
from app_runner.errors.FieldValidationErrors import FieldValidationErrors
from app_runner.field.Field import Field

class TextField(Field):
    _minSize: int
    _maxSize: int

    def __init__(self, properties: dict):
        super().__init__(properties)
        self._minSize = properties.get('min_size')
        self._maxSize = properties.get('max_size')

    # Getter Methods

    def getMaxSize(self) -> int:
        return self._maxSize

    def getMinSize(self) -> int:
        return self._minSize

    # Utility Methods

    def validate(self, value: object, errors: FieldValidationErrors):
        super().validate(value, errors)
        if self.isRequired() and value is None:
            errors.addError(FieldValidationError("Please enter value.", self.getId()))
        else:
            valueStr = str(value)
            if self._maxSize is not None and self._maxSize < len(valueStr):
                errors.addError(FieldValidationError("Field '" + self._id + "' is assigned to string '" + valueStr + "' with size greater than max size '" + str(self._maxSize) + "'.", self.getId()))
            if self._minSize is not None and self._minSize > len(valueStr):
                errors.addError(FieldValidationError("Field '" + self._id + "' is assigned to string '" + valueStr + "' with size less than min size '" + str(self._minSize) + "'.", self.getId()))
