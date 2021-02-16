from src.app.CmdExecAppRunner import CmdExecAppRunner
from tests.src.utils.TestFileUtil import TestFileUtil
from tests.src.utils.TestUtil import TestUtil


class TestDateField:
    __cmdSettings = None
    __fieldSettings = None
    

    def setup_method(self, method):
        self.__fieldSettings = {'id': 'publish_date', 'label': 'Publish Date', 'type': 'date'}
        self.__cmdSettings = {
            'id': 'cmd3',
            'title': 'Command 3',
            'module': 'core',
            'executor': {
                'class': 'TestExecutor3',
                'method': 'run'
            },
            'fields': [self.__fieldSettings]
        }

    @classmethod
    def setup_class(cls):
        TestUtil.setupTestingEnvironment()

    @classmethod
    def teardown_class(cls):
        TestUtil.destroyTestingEnvironment()

    def test_valid_date_field_from_cmd_file_module(self, monkeypatch, capsys):
        # Given
        TestFileUtil.saveCmdFileForModule(self.__cmdSettings, 'cmd3', 'core')
        monkeypatch.setattr('sys.argv', ['pytest', '--cmd', 'cmd3', '--args', 'publish_date:01-01-2021'])
        TestUtil.useExecutorsInModule(['TestExecutor3.py'], 'core')
        # When
        CmdExecAppRunner.run()
        # Then
        response = capsys.readouterr()
        assert 'publish_date=01-01-2021' in response.out

    def test_valid_date_field_from_cmd_file_commands_dir(self, monkeypatch, capsys):
        # Given
        TestFileUtil.saveCmdFileInCommandsDir(self.__cmdSettings, 'cmd3', 'core')
        monkeypatch.setattr('sys.argv', ['pytest', '--cmd', 'cmd3', '--args', 'publish_date:01-01-2021'])
        TestUtil.useExecutorsInModule(['TestExecutor3.py'], 'core')
        # When
        CmdExecAppRunner.run()
        # Then
        response = capsys.readouterr()
        assert 'publish_date=01-01-2021' in response.out

    def test_date_field_value_from_arg_file(self, monkeypatch, capsys):
        # Given
        monkeypatch.setattr('sys.argv', ['pytest', '--cmd', 'cmd3'])
        TestUtil.useExecutorsInModule(['TestExecutor3.py'], 'core')
        TestFileUtil.saveCmdFileInCommandsDir(self.__cmdSettings, 'cmd3', 'core')
        TestFileUtil.saveArgFile({'publish_date': '01-01-2021'}, 'cmd3')
        # When
        CmdExecAppRunner.run()
        # Then
        response = capsys.readouterr()
        assert 'publish_date=01-01-2021' in response.out

    def test_required_date_field_wout_value(self, monkeypatch, capsys):
        # Given
        monkeypatch.setattr('sys.argv', ['pytest', '--cmd', 'cmd3'])
        TestUtil.useExecutorsInModule(['TestExecutor3.py'], 'core')
        self.__fieldSettings['required'] = True
        TestFileUtil.saveCmdFileInCommandsDir(self.__cmdSettings, 'cmd3', 'core')
        # When
        CmdExecAppRunner.run()
        # Then
        response = capsys.readouterr()
        assert 'ERR57' in response.out

    def test_date_field_with_value_out_of_range_1(self, monkeypatch, capsys):
        # Given
        monkeypatch.setattr('sys.argv', ['pytest', '--cmd', 'cmd3'])
        TestUtil.useExecutorsInModule(['TestExecutor3.py'], 'core')
        self.__fieldSettings['min'] = '02-01-2021'
        TestFileUtil.saveCmdFileInCommandsDir(self.__cmdSettings, 'cmd3', 'core')
        TestFileUtil.saveArgFile({'publish_date': '01-01-2021'}, 'cmd3')
        # When
        CmdExecAppRunner.run()
        # Then
        response = capsys.readouterr()
        assert 'ERR56' in response.out

    def test_date_field_with_value_out_of_range_2(self, monkeypatch, capsys):
        # Given
        monkeypatch.setattr('sys.argv', ['pytest', '--cmd', 'cmd3'])
        TestUtil.useExecutorsInModule(['TestExecutor3.py'], 'core')
        self.__fieldSettings['min'] = '02-01-2021'
        self.__fieldSettings['min'] = '03-01-2021'
        TestFileUtil.saveCmdFileInCommandsDir(self.__cmdSettings, 'cmd3', 'core')
        TestFileUtil.saveArgFile({'publish_date': '04-01-2021'}, 'cmd3')
        # When
        CmdExecAppRunner.run()
        # Then
        response = capsys.readouterr()
        assert 'ERR56' in response.out

    def test_date_field_with_invalid_formatted_value(self, monkeypatch, capsys):
        # Given
        monkeypatch.setattr('sys.argv', ['pytest', '--cmd', 'cmd3'])
        TestUtil.useExecutorsInModule(['TestExecutor3.py'], 'core')
        self.__fieldSettings['format'] = '%Y'
        TestFileUtil.saveCmdFileInCommandsDir(self.__cmdSettings, 'cmd3', 'core')
        TestFileUtil.saveArgFile({'publish_date': '04-01-2021'}, 'cmd3')
        # When
        CmdExecAppRunner.run()
        # Then
        response = capsys.readouterr()
        assert 'ERR55' in response.out



