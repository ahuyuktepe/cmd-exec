from classes.errors.FieldValidationError import FieldValidationError
from classes.field.Field import Field
from classes.utils.ListUtil import ListUtil

class MultiSelectField(Field):
    _options: list

    def __init__(self, properties: dict):
        super().__init__(properties)
        self.setOptions(properties.get('options'))

    def setOptions(self, options: list):
        self._options = options

    def getOptions(self) -> list:
        return self._options

    def validate(self, value: object):
        super().validate(value)
        values: list = str(value).split('|')
        for value in values:
            if not ListUtil.hasElementByKey(self._options, 'id', value):
                raise FieldValidationError("Field '" + self._id + "' value '" + value + "' is not in options.")
