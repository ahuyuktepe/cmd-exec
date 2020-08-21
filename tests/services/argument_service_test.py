import sys

from app_runner.services.ArgumentService import ArgumentService
from tests.base_service_test import TestBaseService
from tests.utils.TestConfigUtil import TestConfigUtil
from tests.utils.TestFileUtil import TestFileUtil
from tests.utils.TestUtil import TestUtil


class TestArgumentService(TestBaseService):
    argumentService: ArgumentService

    def test_int_mode_1(self):
        # given
        sys.argv = ['prog']
        self.argumentService = ArgumentService()
        # then
        assert self.argumentService.isInteractiveMode() == True

    def test_int_mode_2(self):
        # given
        sys.argv = ['prog','--mode', 'int']
        self.argumentService = ArgumentService()
        # then
        assert self.argumentService.isInteractiveMode() == True

    def test_cmd_mode(self):
        # given
        sys.argv = ['prog', '--mode', 'cmd']
        self.argumentService = ArgumentService()
        # then
        assert self.argumentService.isCmdMode() == True

    def test_cid_argument(self):
        # given
        sys.argv = ['prog', '--cmd', 'test-command']
        self.argumentService = ArgumentService()
        # then
        assert self.argumentService.getCmd() == 'test-command'

    def test_command_locator(self):
        # given
        TestFileUtil.setRootPath()
        TestFileUtil.createMainConfig(self._test_config)
        TestUtil.setTestScriptArguments(['prog', '--mode', 'cmd', '--cmd', 'test'])
        argumentService = ArgumentService()
        self._initAppContext()
        # when
        cid: str = argumentService.getCmd()
        cmdLocator = TestConfigUtil.getMainCmdLocator(self._appContext, cid)
        # then
        assert cmdLocator['cmd'] == 'test-cmd'
        assert cmdLocator['menu'] == 'test-menu'
        assert cmdLocator['module'] == 'test-module'