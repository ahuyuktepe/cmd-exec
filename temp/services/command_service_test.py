from app_runner.menu.Command import Command
from app_runner.services.CommandService import CommandService
from temp.base_service_test import TestBaseService
from temp.utils.TestFileUtil import TestFileUtil


class TestCommandService(TestBaseService):

    def test_build_command(self):
        # given
        module = 'test'
        menu = 'test-menu'
        self._initAppContext()
        commandService = CommandService()
        commandService._appContext = self._appContext
        TestFileUtil.setRootPath()
        TestFileUtil.createModuleConfig(module, menu, self._menu)
        # when
        cmdLocator = {
            'module': module,
            'menu': menu,
            'cmd': 'test-cmd'
        }
        cmd: Command = commandService.buildCommand(cmdLocator)
        # then
        assert cmd.getId() == 'test-cmd'
        assert cmd.getDescription() == 'Test Command'
        assert cmd.getExecutorClass() == 'TestExecutor'
        assert cmd.getExecutorMethod() == 'executeTestCmd'
        fields: dict = cmd.getFields()
        assert fields['first-name'] is not None
        assert fields['last-name'] is not None
        assert fields['email'] is not None
