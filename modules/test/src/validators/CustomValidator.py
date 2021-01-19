from app_runner.errors.FieldValidationError import FieldValidationError
from app_runner.errors.FieldValidationErrors import FieldValidationErrors
from app_runner.extension.ContextAware import ContextAware
from app_runner.field.Field import Field


class CustomValidator(ContextAware):

    def validate(self, field: Field, value: object, errors: FieldValidationErrors):
        print('CustomValidator.validate')
        print('Field Id :' + field.getId())
        print('Value : ' + str(value))
        # error.addError(FieldValidationError('Test fail message', field.getId()))

    def validateMe(self, field: Field, value: object, errors: FieldValidationErrors):
        self._appContext.getService('logService').info('Validate Me')
        print('Validate Me')
