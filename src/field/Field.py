
class Field:
    _id: str
    _type: str
    _label: str
    _description: str
    _value: object
    _options: list

    def __init__(self, fid: str, ftype: str):
        self._id = fid
        self._type = ftype

    # Setter Methods

    def setOptions(self, options: list):
        self._options = options

    def setProperties(self, props: dict):
        self._label = props.get('label')
        self._description = props.get('description')

    def setValue(self, value: object):
        self._value = value

    # Getter Methods

    def getValue(self) -> object:
        return self._value

    def print(self):
        print('id: ' + self._id + ' | type: ' + self._type + ' | label: ' + self._label)
