import sys
from app_runner.services.ArgumentService import ArgumentService
from temp.base_service_test import TestBaseService
from temp.utils.TestFileUtil import TestFileUtil
from temp.utils.TestUtil import TestUtil


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

    def test_getArgsAsDict(self):
        # given
        sys.argv = ['prog', '--args_str', 'fname:test,lname:user']
        argumentService = ArgumentService()
        # when
        args: dict = argumentService.getArgsAsDict('tst')
        # then
        assert args.get('fname') == 'test'
        assert args.get('lname') == 'user'

    def test_argsFile(self):
        # given
        argsFileName = 'test.yaml'
        args = {
            "fname":"test",
            "lname":"user"
        }
        TestFileUtil.createArgsFile(args, argsFileName)
        sys.argv = ['prog', '--args_file', 'test.yaml']
        argumentService = ArgumentService()
        # when
        args: dict = argumentService.getArgsAsDict('tst')
        # then
        assert args.get('fname') == 'test'
        assert args.get('lname') == 'user'