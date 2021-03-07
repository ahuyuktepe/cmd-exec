from src.app.CmdExecAppRunner import CmdExecAppRunner
from tests.src.utils.TestUtil import TestUtil


class TestSelectionField:
    def setup_method(method):
        TestUtil.setupTestingEnvironment()

    def teardown_method(method):
        TestUtil.destroyTestingEnvironment()

    def test_options_from_option_provider(self, monkeypatch, capsys):
        # Given
        TestUtil.useCmdFilesInCommandsDir(['cmd10'])
        TestUtil.useProvidersInModule(['NameOptionProvider'])
        TestUtil.useExecutorsInModule(['TestExecutor5'])
        # When
        monkeypatch.setattr('sys.argv', ['pytest', '-cmd', 'cmd10', '-name', 'test_from_provider'])
        CmdExecAppRunner.run()
        # Then
        response = capsys.readouterr()
        respStr = response.out.replace('\n', ' ')
        assert 'Running TestExecutor5' in respStr
        assert 'foid > test_from_provider: Test From Provider' in respStr
        assert 'foid > test_from_provider_1: Test From Provider 1' in respStr
        assert 'foid > test_from_provider_1: Test From Provider 1' in respStr
        assert 'foid > opt1: Test Option' in respStr
        assert 'soid > test_from_provider: Test From Provider' in respStr

    def test_selected_option(self, monkeypatch, capsys):
        # Given
        TestUtil.useCmdFilesInCommandsDir(['cmd7'])
        TestUtil.useExecutorsInModule(['TestExecutor5'])
        # When
        monkeypatch.setattr('sys.argv', ['pytest', '-cmd', 'cmd7', '-city', 'ny'])
        CmdExecAppRunner.run()
        # Then
        response = capsys.readouterr()
        respStr = response.out.replace('\n', ' ')
        assert 'Running TestExecutor5' in respStr
        assert 'foid > ny: New York' in respStr
        assert 'foid > london: London' in respStr
        assert 'soid > ny: New York' in respStr

    def test_default_value(self, monkeypatch, capsys):
        # Given
        TestUtil.useCmdFilesInCommandsDir(['cmd7'])
        TestUtil.useExecutorsInModule(['TestExecutor5'])
        # When
        monkeypatch.setattr('sys.argv', ['pytest', '-cmd', 'cmd7'])
        CmdExecAppRunner.run()
        # Then
        response = capsys.readouterr()
        respStr = response.out.replace('\n', ' ')
        assert 'Running TestExecutor5' in respStr
        assert 'foid > tr: Turkey' in respStr
        assert 'foid > usa: United States of America' in respStr
        assert 'soid > usa: United States of America' in respStr

    def test_min_selected(self, monkeypatch, capsys):
        # Given
        TestUtil.useCmdFilesInCommandsDir(['cmd8'])
        TestUtil.useExecutorsInModule(['TestExecutor5'])
        # When
        monkeypatch.setattr('sys.argv', ['pytest', '-cmd', 'cmd8'])
        CmdExecAppRunner.run()
        # Then
        response = capsys.readouterr()
        respStr = response.out.replace('\n', ' ')
        assert 'ERR67' in respStr

    def test_max_selected(self, monkeypatch, capsys):
        # Given
        TestUtil.useCmdFilesInCommandsDir(['cmd9'])
        TestUtil.useExecutorsInModule(['TestExecutor5'])
        # When
        monkeypatch.setattr('sys.argv', ['pytest', '-cmd', 'cmd9', '-name', 'test,test1,test2'])
        CmdExecAppRunner.run()
        # Then
        response = capsys.readouterr()
        respStr = response.out.replace('\n', ' ')
        assert 'ERR68' in respStr
