from src.util.ValidationUtil import ValidationUtil


class Field:
    _id: str
    _type: str
    _label: str
    _value: object
    _options: list
    _default: str
    _isRequired: bool

    def __init__(self, id: str, ftype: str):
        self._id = id
        self._type = ftype
        self._value = None

    # Setter Methods

    def setLabel(self, label: str):
        self._label = label

    def setOptions(self, options: list):
        self._options = options

    def setProperties(self, props: dict):
        label = props.get('label')
        ValidationUtil.failIfNotType(label, str, 'ERR55', {'fid': self._id, 'prop': 'label'})
        self._label = label
        self._default = props.get('default')
        required = str(props.get('required'))
        self._isRequired = required == 'True'

    def setValue(self, value: object):
        self._value = value

    # Getter Methods

    def isRequired(self) -> bool:
        return self._isRequired

    def isRequiredAndHaveNoValue(self) -> bool:
        return self.isRequired() and self._value is None

    def getId(self) -> str:
        return self._id

    def getValue(self) -> object:
        return self._value

    def print(self):
        print('id: ' + self._id + ' | type: ' + self._type + ' | label: ' + self._label + ' | value: ' + str(self._value))
        print('default: ' + str(self._default) + ' | required: ' + str(self._isRequired))
