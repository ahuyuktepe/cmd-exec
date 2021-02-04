from src.app.CmdExecAppRunner import CmdExecAppRunner
from tests.utils.TestModuleUtil import TestModuleUtil


class TestExecApp:
    __services: list = [
        {'id': 'configService', 'path': 'modules.core.src.service.CoreConfigService', 'args': ['appConfigs']},
        {'id': 'argService', 'path': 'modules.core.src.service.CoreArgService', 'args': ['@configService']},
        {'id': 'logService', 'path': 'modules.core.src.service.CoreLogService', 'args': ['@configService']},
        {'id': 'cmdService', 'path': 'modules.core.src.service.CoreCmdService', 'args': []}
    ]
    __configs: dict = {
       'application': {
           'modes': [
               {'id': 'cmd', 'module': 'core', 'runner': 'TestCmdExecApp'}
           ]
        }
    }

    @classmethod
    def teardown_class(cls):
        # TestModuleUtil.clearModulesDir()
        pass

    def prepare_test(self, services: list = None, configs: dict = None):
        testServices = services
        if testServices is None:
            testServices = self.__services
        testConfigs = configs
        if testConfigs is None:
            testConfigs = self.__configs
        TestModuleUtil.clearModulesDir()
        TestModuleUtil.generateModulesDir()
        TestModuleUtil.generateModuleDir('core')
        TestModuleUtil.generateModuleFiles('core', {
            'name': 'core',
            'description': 'Core Module',
            'version': '0.0.1',
            'services': testServices
        }, testConfigs)
        TestModuleUtil.copyModuleFiles(['modules', 'core', 'src', 'service'], ['CoreConfigService.py', 'CoreArgService.py', 'CoreLogService.py', 'CoreCmdService.py'])
        TestModuleUtil.copyFilesFromDummyClasses(['modules', 'core', 'src', 'app'], ['TestCmdExecApp.py'])

    def test_non_existing_exec_app(self, monkeypatch, capsys):
        self.prepare_test()
        monkeypatch.setattr('sys.argv', ['pytest', '--cmd', 'test'])
        TestModuleUtil.copyModuleFiles(['modules', 'core', 'src', 'service'], ['CoreConfigService.py', 'CoreArgService.py', 'CoreLogService.py', 'CoreCmdService.py'])
        CmdExecAppRunner.run()
        response = capsys.readouterr()
        assert 'ERR31' in response.out

    def test_non_existing_exec_app_1(self, monkeypatch, capsys):
        self.prepare_test()
        monkeypatch.setattr('sys.argv', ['pytest', '--cmd', 'test.test'])
        TestModuleUtil.copyModuleFiles(['modules', 'core', 'src', 'service'], ['CoreConfigService.py', 'CoreArgService.py', 'CoreLogService.py', 'CoreCmdService.py'])
        TestModuleUtil.copyModuleFiles(['modules', 'core', 'src', 'app'], ['CoreCmdExecApp.py'])
        CmdExecAppRunner.run()
        response = capsys.readouterr()
        assert 'ERR34' in response.out

    def test_non_existing_exec_app_2(self, monkeypatch, capsys):
        self.prepare_test()
        monkeypatch.setattr('sys.argv', ['pytest', '--cmd', 'core.test'])
        TestModuleUtil.copyModuleFiles(['modules', 'core', 'src', 'app'], ['CoreCmdExecApp.py'])
        CmdExecAppRunner.run()
        response = capsys.readouterr()
        assert 'ERR34' in response.out

    def test_non_existing_mode(self, capsys):
        self.prepare_test(None, {'application': {'name': 'test'}})
        CmdExecAppRunner.run()
        response = capsys.readouterr()
        assert 'ERR43' in response.out

    def test_default_mode(self, monkeypatch, capsys):
        self.prepare_test()
        monkeypatch.setattr('sys.argv', ['pytest', '--cmd', 'core.test'])
        CmdExecAppRunner.run()
        response = capsys.readouterr()
        assert 'TestCmdExecApp is running.' in response.out
