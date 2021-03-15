from src.app.CmdExecAppRunner import CmdExecAppRunner
from tests.src.utils.TestUtil import TestUtil


class TestExecApp:

    def setup_method(method):
        TestUtil.setupTestingEnvironment()

    def teardown_method(method):
        TestUtil.destroyTestingEnvironment()

    def test_non_existing_exec_app(self, monkeypatch, capsys):
        # Given
        monkeypatch.setattr('sys.argv', ['pytest', '-cmd', 'test'])
        TestUtil.buildModuleFiles('test', {'name': 'test', 'version': '0.0.1'}, {
            'application': {
               'modes': [
                   {'id': 'cmd', 'module': 'test1', 'runner': 'TestCmdExecApp'}
               ]
            }
        })
        TestUtil.useAppRunnerInModule(['TestCmdExecApp'], 'test')
        # When
        CmdExecAppRunner.run()
        # Then
        response = capsys.readouterr()
        respStr = response.out.strip('\n')
        assert 'ERR31' in respStr

    def test_non_existing_command_file(self, monkeypatch, capsys):
        # Given
        monkeypatch.setattr('sys.argv', ['pytest', '-cmd', 'test'])
        TestUtil.useConfigFilesInConfigsDir(['main.config.yaml'])
        # When
        CmdExecAppRunner.run()
        # Then
        response = capsys.readouterr()
        respStr = response.out.strip('\n')
        assert 'ERR34' in respStr

    def test_running_custom_cmd_exec_app(self, monkeypatch, capsys):
        # Given
        TestUtil.buildModuleFiles('test', {'name': 'test', 'version': '0.0.1'}, {
            'application': {
                'modes': [
                    {'id': 'test', 'module': 'test', 'runner': 'TestCmdExecApp'}
                ]
            }
        })
        TestUtil.useAppRunnerInModule(['TestCmdExecApp'], 'test')
        # When
        monkeypatch.setattr('sys.argv', ['pytest', '-mode', 'test'])
        CmdExecAppRunner.run()
        # Then
        response = capsys.readouterr()
        assert 'TestCmdExecApp is running.' in response.out
