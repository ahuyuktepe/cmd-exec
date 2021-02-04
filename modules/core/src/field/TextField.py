from src.field.Field import Field


class TextField(Field):

    def __init__(self, fid: str):
        super().__init__(fid, 'text')

    def print(self):
        print('TextField => id: ' + self._id + ' | type: ' + self._type + ' | label: ' + self._label)
