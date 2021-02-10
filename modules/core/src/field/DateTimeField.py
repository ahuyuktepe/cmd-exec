from src.field.Field import Field
from src.field.FieldType import FieldType
from src.util.ValidationUtil import ValidationUtil


class DateTimeField(Field):
    _format: str

    def __init__(self, fid: str):
        super().__init__(fid, FieldType.DATE_TIME)

    def setProperties(self, props: dict):
        super().setProperties(props)
        dateFormat = props.get('format')
        ValidationUtil.failIfNotType(dateFormat, str, 'ERR55', {'fid': self._id, 'prop': 'format'})
        self._format = dateFormat

    def print(self):
        print("=======================================================================================================")
        print('DateField => id: ' + self._id + ' | type: ' + self._type + ' | label: ' + self._label)
        print('Value: ' + str(self._value))
