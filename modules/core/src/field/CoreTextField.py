from src.error.CmdExecError import CmdExecError
from src.enum.FieldType import FieldType
from src.field.TextField import TextField


class CoreTextField(TextField):
    _value: str
    _default: str
    _minSize: int
    _maxSize: int

    def __init__(self, fid: str):
        super().__init__(fid, FieldType.TEXT)
        self._minSize = None
        self._maxSize = None

    def setValue(self, value: str):
        if value is None and self._default is not None:
            self._value = self._default
        else:
            self._value = value

    def setProperties(self, props: dict):
        super().setProperties(props)
        self.__setMinSize(props)
        self.__setMaxSize(props)

    def validate(self):
        super().validate()
        if self._minSize is not None and len(self._value) < self._minSize:
            raise CmdExecError('ERR61', {'value': self._value, 'fid': self.getId(), 'min_size': str(self._minSize)})
        if self._maxSize is not None and len(self._value) > self._maxSize:
            raise CmdExecError('ERR62', {'value': self._value, 'fid': self.getId(), 'max_size': str(self._maxSize)})

    def _setDefault(self, props: dict):
        self._default = props.get('default')

    def __setMinSize(self, props: dict):
        value = props.get('min_size')
        if value is not None and not isinstance(value, int):
            raise CmdExecError('ERR55', {'fid': self.getId(), 'prop': 'min_size'})
        self._minSize = value

    def __setMaxSize(self, props: dict):
        value = props.get('max_size')
        if value is not None and not isinstance(value, int):
            raise CmdExecError('ERR55', {'fid': self.getId(), 'prop': 'max_size'})
        self._maxSize = value

    def getValue(self) -> str:
        return self._value

    def print(self):
        print("====================================== Text Field =========================================")
        print("--- Common Properties ---")
        super().print()
        print("--- Text Field Properties ---")
        print('Value: ' + self._value)
