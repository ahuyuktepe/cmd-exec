from app_runner.extension.ContextAware import ContextAware
from app_runner.field.Field import Field


class CustomValidator(ContextAware):

    def validate(self, field: Field, value: object):
        print('CustomValidator.validate')
        print('Field Id :' + field.getId())
        print('Value : ' + str(value))

    def validateMe(self, field: Field, value: object):
        self._appContext.getService('logService').info('Validate Me')
        print('Validate Me')
