from app_runner.field.Field import Field
import datetime
from app_runner.utils.DataUtil import DataUtil

class DateTimeField(Field):
    _format: str

    def __init__(self, properties: dict):
        super().__init__(properties)
        self._format = str(DataUtil.getDefaultIfNone(properties.get('format'), '%m-%d-%Y %H:%M:%S'))

    def validate(self, value: object):
        super().validate(value)
        dateStr: str = str(value)
        datetime.datetime.strptime(dateStr, self._format)

    def getDefaultValueIfNone(self, value: object) -> object:
        val = super().getDefaultValueIfNone(value)
        valStr: str = str(val)
        if valStr == 'now':
            return datetime.datetime.now().strftime(self._format)
        return valStr

    def getFormat(self) -> str:
        return self._format
