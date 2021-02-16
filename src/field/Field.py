from src.error.CmdExecError import CmdExecError
from src.util.ValidationUtil import ValidationUtil


class Field:
    _id: str
    _type: str
    _label: str
    _required: bool

    def __init__(self, id: str, ftype: str):
        self._id = id
        self._type = ftype
        self._value = None
        self._required = False
        self._default = None
        self._min = None
        self._max = None

    def setProperties(self, props: dict):
        # Set label field
        label = props.get('label')
        self.setLabel(label)
        # Set required field
        required = props.get('required')
        self._setRequired(required)

    def setLabel(self, label: object):
        ValidationUtil.failIfNotType(label, str, 'ERR55', {'fid': self._id, 'prop': 'label'})
        self._label = str(label)

    def _setRequired(self, value: object):
        if value is not None:
            ValidationUtil.failIfNotType(value, bool, 'ERR55', {'fid': self._id, 'prop': 'required'})
            self._required = str(value) == 'True'

    def isRequired(self) -> bool:
        return self._required

    def isRequiredAndHaveNoValue(self) -> bool:
        return self.isRequired() and self._value is None

    def getId(self) -> str:
        return self._id

    def validate(self):
        if self.isRequired() and self._value is None:
            raise CmdExecError('ERR57', {'fid': self._id})

    def print(self):
        print('id: ' + self._id + ' | type: ' + self._type + ' | label: ' + self._label + ' | required: ' + str(self._required))
