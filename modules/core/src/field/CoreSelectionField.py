from src.enum.FieldType import FieldType
from src.field.SelectionField import SelectionField
from src.util.ValidationUtil import ValidationUtil


class SingleSelectField(SelectionField):
    _options: list

    def __init__(self, fid: str):
        super().__init__(fid, FieldType.SELECTION)

    def setOptions(self, options: list):
        ValidationUtil.failIfNotType(options, list, 'ERR55', {'fid': self._id, 'prop': 'options'})
        self._options = options

    def validate(self):
        print('validating SingleSelectField')

    def print(self):
        print("====================================== Selection Field =========================================")
        print("--- Common Properties ---")
        super().print()
        print("--- Selection Field Properties ---")
        print('options: ' + str(self._options))
