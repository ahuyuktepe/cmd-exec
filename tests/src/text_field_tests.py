from src.app.CmdExecAppRunner import CmdExecAppRunner
from tests.src.utils.TestFileUtil import TestFileUtil
from tests.src.utils.TestUtil import TestUtil


class TestTextField:
    __cmdSettings = None
    __fieldSettings = None

    def setup_method(self):
        self.__fieldSettings = {'id': 'name', 'label': 'Test Field', 'type': 'text'}
        self.__cmdSettings = {
            'id': 'cmd1',
            'title': 'Command 1',
            'module': 'core',
            'executor': {
                'class': 'TestExecutor',
                'method': 'run'
            },
            'fields': [self.__fieldSettings]
        }
        TestUtil.setupTestingEnvironment()

    def teardown_method(method):
        TestUtil.destroyTestingEnvironment()

    def test_default_value(self, monkeypatch, capsys):
        # Given
        TestFileUtil.removeArgFile('cmd1')
        TestFileUtil.removeCmdFileForModule('cmd1', 'core')
        TestUtil.useExecutorsInModule(['TestExecutor'], 'core')
        self.__fieldSettings['default'] = 'Default Value'
        TestFileUtil.saveCmdFileInCommandsDir(self.__cmdSettings, 'cmd1')
        # When
        monkeypatch.setattr('sys.argv', ['pytest', '-cmd', 'cmd1'])
        CmdExecAppRunner.run()
        # Then
        response = capsys.readouterr()
        respStr = response.out.strip('\n')
        assert 'cls: TestExecutor, method: run' in respStr and 'name=Default Value' in respStr

    def test_default_value_greater_then_max_size(self, monkeypatch, capsys):
        # Given
        TestFileUtil.removeArgFile('cmd1')
        TestFileUtil.removeCmdFileForModule('cmd1', 'core')
        TestUtil.useExecutorsInModule(['TestExecutor'], 'core')
        self.__fieldSettings['default'] = 'Default Value'
        self.__fieldSettings['max_size'] = 5
        TestFileUtil.saveCmdFileInCommandsDir(self.__cmdSettings, 'cmd1')
        # When
        monkeypatch.setattr('sys.argv', ['pytest', '-cmd', 'cmd1'])
        CmdExecAppRunner.run()
        # Then
        response = capsys.readouterr()
        respStr = response.out.strip('\n')
        assert 'ERR62' in respStr

    def test_valid_date_field_from_cmd_file_module(self, monkeypatch, capsys):
        # Given
        TestFileUtil.saveCmdFileForModule(self.__cmdSettings, 'cmd1', 'core')
        TestUtil.useExecutorsInModule(['TestExecutor'], 'core')
        # When
        monkeypatch.setattr('sys.argv', ['pytest', '-cmd', 'cmd1', '-name', 'test'])
        CmdExecAppRunner.run()
        # Then
        response = capsys.readouterr()
        respStr = response.out.strip('\n')
        assert 'cls: TestExecutor, method: run' in respStr and 'name=test' in respStr

    def test_required_date_field_wout_value(self, monkeypatch, capsys):
        # Given
        TestFileUtil.removeArgFile('cmd1')
        TestFileUtil.removeCmdFileForModule('cmd1', 'core')
        TestUtil.useExecutorsInModule(['TestExecutor'], 'core')
        self.__fieldSettings['required'] = True
        TestFileUtil.saveCmdFileInCommandsDir(self.__cmdSettings, 'cmd1')
        # When
        monkeypatch.setattr('sys.argv', ['pytest', '-cmd', 'cmd1'])
        CmdExecAppRunner.run()
        # Then
        response = capsys.readouterr()
        assert 'ERR57' in response.out

    def test_invalid_min_size_value(self, monkeypatch, capsys):
        # Given
        TestFileUtil.removeArgFile('cmd1')
        TestFileUtil.removeCmdFileForModule('cmd1', 'core')
        TestUtil.useExecutorsInModule(['TestExecutor'], 'core')
        self.__fieldSettings['min_size'] = 'test'
        TestFileUtil.saveCmdFileInCommandsDir(self.__cmdSettings, 'cmd1')
        # When
        monkeypatch.setattr('sys.argv', ['pytest', '-cmd', 'cmd1'])
        CmdExecAppRunner.run()
        # Then
        response = capsys.readouterr()
        assert 'ERR55' in response.out

    def test_invalid_max_size_value(self, monkeypatch, capsys):
        # Given
        TestFileUtil.removeArgFile('cmd1')
        TestFileUtil.removeCmdFileForModule('cmd1', 'core')
        TestUtil.useExecutorsInModule(['TestExecutor'], 'core')
        self.__fieldSettings['max_size'] = 'test'
        TestFileUtil.saveCmdFileInCommandsDir(self.__cmdSettings, 'cmd1')
        # When
        monkeypatch.setattr('sys.argv', ['pytest', '-cmd', 'cmd1'])
        CmdExecAppRunner.run()
        # Then
        response = capsys.readouterr()
        assert 'ERR55' in response.out

    def test_value_size_less_than_min_size(self, monkeypatch, capsys):
        # Given
        TestFileUtil.removeArgFile('cmd1')
        TestFileUtil.removeCmdFileForModule('cmd1', 'core')
        TestUtil.useExecutorsInModule(['TestExecutor'], 'core')
        self.__fieldSettings['min_size'] = 10
        TestFileUtil.saveCmdFileInCommandsDir(self.__cmdSettings, 'cmd1')
        # When
        monkeypatch.setattr('sys.argv', ['pytest', '-cmd', 'cmd1', '-name', 'test'])
        CmdExecAppRunner.run()
        # Then
        response = capsys.readouterr()
        assert 'ERR61' in response.out

    def test_value_size_greater_than_max_size(self, monkeypatch, capsys):
        # Given
        TestFileUtil.removeArgFile('cmd1')
        TestFileUtil.removeCmdFileForModule('cmd1', 'core')
        TestUtil.useExecutorsInModule(['TestExecutor'], 'core')
        self.__fieldSettings['max_size'] = 5
        TestFileUtil.saveCmdFileInCommandsDir(self.__cmdSettings, 'cmd1')
        # When
        monkeypatch.setattr('sys.argv', ['pytest', '-cmd', 'cmd1', '-name', 'This is a test value'])
        CmdExecAppRunner.run()
        # Then
        response = capsys.readouterr()
        assert 'ERR62' in response.out
