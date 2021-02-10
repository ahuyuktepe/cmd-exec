from src.field.Field import Field
from src.field.FieldType import FieldType
from src.util.ValidationUtil import ValidationUtil


class DateField(Field):
    _format: str

    def __init__(self, fid: str):
        super().__init__(fid, FieldType.DATE)

    def setProperties(self, props: dict):
        super().setProperties(props)
        dateFormat = props.get('format')
        ValidationUtil.failIfNotType(dateFormat, str, 'ERR55', {'fid': self._id, 'prop': 'format'})
        self._format = dateFormat

    def print(self):
        print("====================================== Date Field =========================================")
        print("--- Common Properties ---")
        super().print()
        print("--- Date Field Properties ---")
        print('format: ' + self._format)
