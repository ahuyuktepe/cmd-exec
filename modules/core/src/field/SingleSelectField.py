from src.field.Field import Field


class SingleSelectField(Field):

    def __init__(self, fid: str):
        super().__init__(fid, 'single_select')

    def print(self):
        print('SingleSelectField => id: ' + self._id + ' | type: ' + self._type + ' | label: ' + self._label)
        for option in self._options:
            option.print()