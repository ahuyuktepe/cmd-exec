from app_runner.errors.FieldValidationError import FieldValidationError
from app_runner.menu.Command import Command
from app_runner.services.CommandService import CommandService
from app_runner.services.FieldService import FieldService
from app_runner.utils.ListUtil import ListUtil
from tests.base_service_test import TestBaseService
import pytest


class TestFieldService(TestBaseService):
    fieldService: FieldService
    cmdService: CommandService

    def setup(self):
        self._initAppContext()
        self.cmdService = self._appContext.getService('commandService')
        self.fieldService = self._appContext.getService('fieldService')

    def test_validateFieldValues(self):
        self.setup()
        cmds = self._menu.get('commands')
        cmdObj = ListUtil.getElementByKey(cmds, 'id', 'test-cmd')
        cmd: Command = self.cmdService.buildCmd(cmdObj)
        self.fieldService.insertFields(cmd, cmdObj.get('fields'))
        fieldValues: dict = {
            'first-name': 'Test',
            'last-name': 'User'
        }
        fields: dict = cmd.getFields()
        with pytest.raises(FieldValidationError) as validationError:
            self.fieldService.validateFieldValues(fields, fieldValues)
