from src.app.CmdExecAppRunner import CmdExecAppRunner
from tests.src.utils.TestUtil import TestUtil


class TestCmdExecutor:

    def setup_method(method):
        TestUtil.setupTestingEnvironment()
        TestUtil.buildModuleFiles('test', {
            'name': 'test',
            'version': '0.0.1'
        })
        TestUtil.useConfigFilesInConfigsDir(['main.config.yaml'])

    def teardown_method(method):
        # TestUtil.destroyTestingEnvironment()
        pass

    def test_non_existing_cmd_execution(self, monkeypatch, capsys):
        # Given
        monkeypatch.setattr('sys.argv', ['pytest', '-cmd', 'cmd1'])
        # When
        CmdExecAppRunner.run()
        # Then
        response = capsys.readouterr()
        assert 'ERR34' in response.out

    def test_non_existing_executor_class(self, monkeypatch, capsys):
        # Given
        monkeypatch.setattr('sys.argv', ['pytest', '-cmd', 'test.cmd1'])
        TestUtil.useCmdFilesInModule(['cmd1'], 'test')
        # When
        CmdExecAppRunner.run()
        # Then
        response = capsys.readouterr()
        assert 'ERR51' in response.out

    def test_executor_class_not_extended(self, monkeypatch, capsys):
        # Given
        monkeypatch.setattr('sys.argv', ['pytest', '-cmd', 'test.cmd2'])
        TestUtil.useCmdFilesInModule(['cmd2'], 'test')
        TestUtil.useExecutorsInModule(['TestExecutor2'], 'test')
        # When
        CmdExecAppRunner.run()
        # Then
        response = capsys.readouterr()
        assert 'ERR59' in response.out

    def test_cmd_execution(self, monkeypatch, capsys):
        # Given
        monkeypatch.setattr('sys.argv', ['pytest', '-cmd', 'test.cmd1'])
        TestUtil.useCmdFilesInModule(['cmd1'], 'test')
        TestUtil.useExecutorsInModule(['TestExecutor1'], 'test')
        # When
        CmdExecAppRunner.run()
        # Then
        response = capsys.readouterr()
        respStr = response.out.strip('\n')
        assert respStr == 'Running TestExecutor1'

    def testing_custom_exec_command_in_executor_cls(self, monkeypatch, capsys):
        # Given
        TestUtil.useCmdFilesInModule(['cmd5'], 'test')
        TestUtil.useExecutorsInModule(['TestExecutor5'], 'test')
        monkeypatch.setattr('sys.argv', ['pytest', '-cmd', 'test.cmd5', '-publish_date', '01-01-2021'])
        # When
        CmdExecAppRunner.run()
        # Then
        response = capsys.readouterr()
        respStr = response.out.strip('\n')
        assert 'Running TestExecutor5' in respStr and 'publish_date=01-01-2021' in respStr
