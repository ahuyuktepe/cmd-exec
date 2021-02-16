from src.app.CmdExecAppRunner import CmdExecAppRunner
from tests.src.utils.TestUtil import TestUtil


class TestCmdExecutor:
    @classmethod
    def setup_class(cls):
        TestUtil.setupTestingEnvironment()

    @classmethod
    def teardown_class(cls):
        TestUtil.destroyTestingEnvironment()

    def test_non_existing_cmd_execution(self, monkeypatch, capsys):
        # Given
        monkeypatch.setattr('sys.argv', ['pytest', '--cmd', 'cmd1'])
        # When
        CmdExecAppRunner.run()
        # Then
        response = capsys.readouterr()
        assert 'ERR34' in response.out

    def test_non_existing_executor_class(self, monkeypatch, capsys):
        # Given
        monkeypatch.setattr('sys.argv', ['pytest', '--cmd', 'cmd1'])
        TestUtil.useCmdFilesInModule(['cmd1.yaml'], 'core')
        # When
        CmdExecAppRunner.run()
        # Then
        response = capsys.readouterr()
        assert 'ERR51' in response.out

    def test_executor_class_not_extended(self, monkeypatch, capsys):
        # Given
        monkeypatch.setattr('sys.argv', ['pytest', '--cmd', 'cmd2'])
        TestUtil.useCmdFilesInModule(['cmd2.yaml'], 'core')
        TestUtil.useExecutorsInModule(['TestExecutor2.py'], 'core')
        # When
        CmdExecAppRunner.run()
        # Then
        response = capsys.readouterr()
        assert 'ERR59' in response.out

    def test_cmd_execution(self, monkeypatch, capsys):
        # Given
        monkeypatch.setattr('sys.argv', ['pytest', '--cmd', 'cmd1'])
        TestUtil.useCmdFilesInModule(['cmd1.yaml'], 'core')
        TestUtil.useExecutorsInModule(['TestExecutor1.py'], 'core')
        # When
        CmdExecAppRunner.run()
        # Then
        response = capsys.readouterr()
        respStr = response.out.strip('\n')
        assert respStr == 'Running TestExecutor1'
