from src.field.Field import Field
from src.field.FieldType import FieldType


class SingleSelectField(Field):

    def __init__(self, fid: str):
        super().__init__(fid, FieldType.SINGLE_SELECT)

    def print(self):
        print("=======================================================================================================")
        print('SingleSelectField => id: ' + self._id + ' | type: ' + self._type + ' | label: ' + self._label)
        print('Value: ' + str(self._value))
