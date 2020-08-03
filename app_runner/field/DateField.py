from app_runner.errors.FieldValidationErrors import FieldValidationErrors
from app_runner.field.Field import Field
import datetime
from app_runner.utils.DataUtil import DataUtil

class DateField(Field):
    _format: str

    def __init__(self, properties: dict):
        super().__init__(properties)
        self._format = DataUtil.getDefaultIfNone(properties.get('format'), 'YYYY-MM-DD')

    def validate(self, value: object, errors: FieldValidationErrors):
        super().validate(value, errors)
        dateStr: str = str(value)
        datetime.datetime.strptime(dateStr, self._format)

    def getDefaultValueIfNone(self, value: object) -> object:
        val = super().getDefaultValueIfNone(value)
        valStr: str = str(val)
        if valStr == 'today':
            return datetime.datetime.today().strftime(self._format)
        return valStr

    def getFormat(self) -> str:
        return self._format
