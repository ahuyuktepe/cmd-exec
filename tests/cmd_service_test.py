from app_runner.menu.Command import Command
from app_runner.services.CommandService import CommandService
from app_runner.services.FieldService import FieldService
from app_runner.utils.ListUtil import ListUtil
from tests.base_service_test import TestBaseService


class TestCmdService(TestBaseService):
    cmdService: CommandService
    fieldService: FieldService

    def setup(self):
        self._initAppContext()
        self.cmdService = self._appContext.getService('commandService')
        self.fieldService = self._appContext.getService('fieldService')

    def test_buildCmd(self):
        self.setup()


        assert cmd.getId() == 'test-cmd'

    def test_getValuesWithDefaultValues(self):
        self.setup()
        cmds = self._menu.get('commands')
        cmdObj = ListUtil.getElementByKey(cmds, 'id', 'test-cmd')
        cmd: Command = self.cmdService.buildCmd(cmdObj)
        self.fieldService.insertFields(cmd, cmdObj.get('fields'))
        fieldValues = {
            "first-name": "Test"
        }
        fieldValues = self.cmdService.getValuesWithDefaultValues(fieldValues, cmd)
        assert fieldValues.get('first-name') == 'Test'
        assert fieldValues.get('last-name') == 'User'

