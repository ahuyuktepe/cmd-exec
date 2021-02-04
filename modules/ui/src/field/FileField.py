from src.field.Field import Field


class FileField(Field):

    def __init__(self, id: str):
        super().__init__(id, 'file')

    def print(self):
        print('FileField => id: ' + self._id + ' | type: ' + self._type + ' | label: ' + self._label)
