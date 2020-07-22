from app_runner.errors.FieldValidationError import FieldValidationError
from app_runner.field.Field import Field

class NumberField(Field):
    _min: int
    _max: int

    def __init__(self, properties: dict):
        super().__init__(properties)
        self._min = properties.get('min')
        self._max = properties.get('max')

    def validate(self, value: object):
        super().validate(value)
        valueStr: str = str(value)
        if not valueStr.isnumeric():
            raise FieldValidationError("Field '" + self._id + "' is number type but value is not number.")
        valueInt: int = int(valueStr)
        if self._min is not None and valueInt < self._min:
            raise FieldValidationError("Field '" + self._id + "' is assigned to value '" + valueStr + "' which is less than min '" + str(self._min) + "'.")
        elif self._max is not None and valueInt > self._max:
            raise FieldValidationError("Field '" + self._id + "' is assigned to value '" + valueStr + "' which is greater than max '" + str(self._max) + "'.")