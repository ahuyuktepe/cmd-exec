
class FieldValues:
    _values: dict

    def __init__(self):
        self._values = {}

    # Setter Methods

    def addValue(self, id: str, value: object):
        self._values[id] = value

    # Getter Methods

    def getValue(self, id: str) -> object:
        return self._values[id]

    def print(self):
        print('Field Values => ' + str(self._values))
