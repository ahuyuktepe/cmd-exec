from src.classes.File import File
from src.error.CmdExecError import CmdExecError
from src.field.Field import Field
from src.field.FieldType import FieldType
from src.util.FileUtil import FileUtil
from src.util.ValidationUtil import ValidationUtil


class CoreFileField(Field):
    _file: File

    def __init__(self, fid: str):
        super().__init__(fid, FieldType.FILE)

    def setValue(self, path: str):
        if path is not None:
            ValidationUtil.failIfNotType(path, str, 'ERR55', {'fid': self._id, 'prop': 'value'})
            arr = FileUtil.fromStrPathToArr(path)
            ValidationUtil.failIfFileCanNotBeAccessed(arr, 'ERR58', {'file': path})
            self._file = File(arr)
        else:
            self._file = None

    def setProperties(self, props: dict):
        self._setDefault(props)

    def _setDefault(self, props: dict):
        try:
            path = props.get('default')
            if path is not None:
                self.setValue(path)
            else:
                self._default = None
        except Exception as exception:
            raise CmdExecError('ERR55',  {'fid': self._id, 'prop': 'default'})

    def getValue(self) -> File:
        return self._file

    def print(self):
        print("====================================== File Field =========================================")
        print("--- Common Properties ---")
        super().print()
        print("--- File Field Properties ---")
        print('File: ' + self._file.toString())
