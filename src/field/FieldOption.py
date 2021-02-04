
class FieldOption:
    _id: str
    _label: str

    def __init__(self, id: str, label: str):
        self._id = id
        self._label = label

    def print(self):
        print('Option => id: ' + self._id + ' | label: ' + self._label)