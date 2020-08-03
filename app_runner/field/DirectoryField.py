from app_runner.errors.FieldValidationError import FieldValidationError
from app_runner.errors.FieldValidationErrors import FieldValidationErrors
from app_runner.field.Field import Field
from app_runner.utils.FileUtil import FileUtil

class DirectoryField(Field):
    _path: str

    def __init__(self, properties: dict):
        super().__init__(properties)
        self._path = properties.get('path')

    def validate(self, value: object, errors: FieldValidationErrors):
        super().validate(value, errors)
        if value is not None:
            path: str = str(value)
            if not FileUtil.doesFileExist(path):
                errors.addError(FieldValidationError("Directory with path '" + str(value) + "' set for field '" + self._id + "' does not exist."))
            elif not FileUtil.isDirectory(path):
                errors.addError(FieldValidationError("Path '" + path + "' set for field '" + self._id + "' is not a directory."))

