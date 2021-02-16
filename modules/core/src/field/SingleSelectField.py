from src.field.Field import Field
from src.field.FieldType import FieldType
from src.util.ValidationUtil import ValidationUtil


class SingleSelectField(Field):
    _options: list

    def __init__(self, fid: str):
        super().__init__(fid, FieldType.SINGLE_SELECT)

    def setOptions(self, options: list):
        ValidationUtil.failIfNotType(options, list, 'ERR55', {'fid': self._id, 'prop': 'options'})
        self._options = options

    def validate(self):
        print('validating SingleSelectField')

    def print(self):
        print("====================================== Single Select Field =========================================")
        print("--- Common Properties ---")
        super().print()
        print("--- Date Field Properties ---")
        print('options: ' + str(self._options))
