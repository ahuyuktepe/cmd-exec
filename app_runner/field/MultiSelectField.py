from app_runner.errors.FieldValidationError import FieldValidationError
from app_runner.errors.FieldValidationErrors import FieldValidationErrors
from app_runner.field.SingleSelectField import SingleSelectField
from app_runner.utils.ListUtil import ListUtil


class MultiSelectField(SingleSelectField):

    def __init__(self, properties: dict):
        super().__init__(properties)

    def validate(self, value: object, errors: FieldValidationErrors):
        values: list = str(value).split('|')
        for value in values:
            if not ListUtil.hasElementByKey(self._options, 'id', value):
                errors.addError(FieldValidationError("Field '" + self._id + "' value '" + value + "' is not in options.", self.getId()))
