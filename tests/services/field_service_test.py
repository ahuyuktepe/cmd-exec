import sys

from app_runner.errors.FieldValidationErrors import FieldValidationErrors
from app_runner.field.Field import Field
from app_runner.field.SingleSelectField import SingleSelectField
from app_runner.menu.Command import Command
from app_runner.services.FieldService import FieldService
from tests.base_service_test import TestBaseService


class TestFieldService(TestBaseService):
    fieldService: FieldService

    def setup(self):
        sys.argv = ['prog', '--cmd', 'test-command']
        self._initAppContext()
        self.fieldService = self._appContext.getService('fieldService')

    def test_getFieldValues(self):
        # given
        cmd = Command('test', None, None, None)
        cmd.addField(Field({'id': 'first-name', 'label': 'First Name'}))
        cmd.addField(Field({'id': 'last-name', 'label': 'Last Name'}))
        # when
        values: dict = self.fieldService.getFieldValues(cmd)
        # then
        assert values.get('first-name') == 'test'
        assert values.get('last-name') == 'user'

    def test_getDefaultFieldValues(self):
        # given
        fields = {
            'first-name': Field({'id': 'first-name', 'label': 'First Name', 'default': 'Default First Name'}),
            'last-name': Field({'id': 'last-name', 'label': 'Last Name', 'default': 'Default Last Name'})
        }
        # when
        defaultValues = self.fieldService.getDefaultFieldValues(fields)
        # then
        assert defaultValues.get('first-name') == 'Default First Name'
        assert defaultValues.get('last-name') == 'Default Last Name'
    def test_validateFieldValues(self):
        # given
        cmd = Command('test', 'Test command', None, None)
        cmd.addField(Field({'id': 'first-name', 'label': 'First Name', 'required': True}))
        fieldValues = {
            'last-name': 'User'
        }
        # when
        errors: FieldValidationErrors = self.fieldService.validateFieldValues(cmd, fieldValues)
        # then
        assert errors.hasErrors() == True

    def test_insertFields(self):
        # given
        cmd = Command('test', 'Test command', None, None)
        fields: list = [
            {'id': 'first-name', 'label': 'First Name', 'type': 'text'},
            {'id': 'last-name', 'label': 'Last Name', 'type': 'text'}
        ]
        # when
        self.fieldService.insertFields(cmd, fields)
        # then
        fields: dict = cmd.getFields()
        assert fields.get('first-name').getLabel() == 'First Name'
        assert fields.get('last-name').getLabel() == 'Last Name'

    def test_setFieldOptions(self):
        # given
        field: Field = SingleSelectField({'id': 'first-name', 'label': 'First Name', 'required': True})
        options = [
            {'id': 1, 'label': 'test1'}
        ]
        # when
        self.fieldService.setFieldOptions(field, 'test', options)
        # then
        assert field.hasOptions() == True