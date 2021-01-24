from src.app.CmdExecAppRunner import CmdExecAppRunner
from tests.utils.TestModuleUtil import TestModuleUtil


class TestExecApp:
    @classmethod
    def teardown_class(cls):
        TestModuleUtil.clearModulesDir()

    def prepare_test(self):
        TestModuleUtil.clearModulesDir()
        TestModuleUtil.generateModulesDir()
        TestModuleUtil.generateModuleDir('core')
        TestModuleUtil.generateModuleFiles('core', {
            'name': 'core',
            'description': 'Core Module',
            'version': '0.0.1',
            'services': [
                {'id': 'configService', 'path': 'modules.core.src.service.CoreConfigService', 'args': ['appConfigs']},
                {'id': 'argService', 'path': 'modules.core.src.service.CoreArgService', 'args': ['@configService']},
                {'id': 'logService', 'path': 'modules.core.src.service.CoreLogService', 'args': ['@configService']},
                {'id': 'cmdService', 'path': 'modules.core.src.service.CoreCmdService', 'args': []}
            ]
        }, {
               'application': {
                   'modes': [
                       {'id': 'cmd', 'module': 'core', 'runner': 'CoreCmdExecApp'}
                   ]
               }
        })
        TestModuleUtil.copyModuleFiles(['modules', 'core', 'src', 'service'], ['CoreConfigService.py', 'CoreArgService.py', 'CoreLogService.py', 'CoreCmdService.py'])

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
