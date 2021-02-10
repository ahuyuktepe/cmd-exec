from src.field.Field import Field
from src.field.FieldType import FieldType


class FileField(Field):

    def __init__(self, fid: str):
        super().__init__(fid, FieldType.FILE)

    def print(self):
        print("=======================================================================================================")
        print('FileField => id: ' + self._id + ' | type: ' + self._type + ' | label: ' + self._label)
        print('Value: ' + str(self._value))
