from src.field.Field import Field
from src.field.FieldType import FieldType


class TextField(Field):

    def __init__(self, fid: str):
        super().__init__(fid, FieldType.TEXT)

    def print(self):
        print("=======================================================================================================")
        print('TextField => id: ' + self._id + ' | type: ' + self._type + ' | label: ' + str(self._label))
        print('Value: ' + str(self._value))
