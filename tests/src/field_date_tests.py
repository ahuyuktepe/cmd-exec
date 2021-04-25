from cmd_exec.app.CmdExecAppRunner import CmdExecAppRunner
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
            'module': 'test',
            'executor': {
                'class': 'TestExecutor3',
                'method': 'run'
            },
            'fields': [self.__fieldSettings]
        }
        TestUtil.setupTestingEnvironment()
        TestUtil.buildModuleFiles('test', {
            'name': 'test',
            'version': '0.0.1'
        })
        TestUtil.useConfigFilesInConfigsDir(['main.config.yaml'])

    def teardown_method(method):
        TestUtil.destroyTestingEnvironment()

    def test_valid_date_field_from_cmd_file_module(self, monkeypatch, capsys):
        # Given
        TestFileUtil.saveCmdFileForModule(self.__cmdSettings, 'cmd3', 'test')
        monkeypatch.setattr('sys.argv', ['pytest', '-cmd', 'test.cmd3', '-publish_date', '01-01-2021'])
        TestUtil.useExecutorsInModule(['TestExecutor3'], 'test')
        # When
        CmdExecAppRunner.run('test')
        # Then
        response = capsys.readouterr()
        respStr = response.out.strip('\n')
        assert 'Running TestExecutor3' in respStr and 'publish_date=01-01-2021' in respStr

    def test_valid_date_field_from_cmd_file_commands_dir(self, monkeypatch, capsys):
        # Given
        TestFileUtil.saveCmdFileInCommandsDir(self.__cmdSettings, 'cmd3')
        monkeypatch.setattr('sys.argv', ['pytest', '-cmd', 'cmd3', '-publish_date', '01-01-2021'])
        TestUtil.useExecutorsInModule(['TestExecutor3'], 'test')
        # When
        CmdExecAppRunner.run('test')
        # Then
        response = capsys.readouterr()
        respStr = response.out.strip('\n')
        assert 'Running TestExecutor3' in respStr and 'publish_date=01-01-2021' in response.out

    def test_date_field_value_from_arg_file(self, monkeypatch, capsys):
        # Given
        monkeypatch.setattr('sys.argv', ['pytest', '-cmd', 'cmd3'])
        TestUtil.useExecutorsInModule(['TestExecutor3'], 'test')
        TestFileUtil.saveCmdFileInCommandsDir(self.__cmdSettings, 'cmd3')
        TestFileUtil.saveArgFile({'publish_date': '01-01-2021'}, 'cmd3')
        # When
        CmdExecAppRunner.run('test')
        # Then
        response = capsys.readouterr()
        respStr = response.out.strip('\n')
        assert 'Running TestExecutor3' in respStr and 'publish_date=01-01-2021' in response.out

    def test_required_date_field_wout_value(self, monkeypatch, capsys):
        # Given
        TestFileUtil.removeArgFile('cmd3')
        TestFileUtil.removeCmdFileForModule('cmd3', 'test')
        monkeypatch.setattr('sys.argv', ['pytest', '-cmd', 'cmd3'])
        TestUtil.useExecutorsInModule(['TestExecutor3'], 'test')
        self.__fieldSettings['required'] = True
        TestFileUtil.saveCmdFileInCommandsDir(self.__cmdSettings, 'cmd3')
        # When
        CmdExecAppRunner.run('test')
        # Then
        response = capsys.readouterr()
        assert 'ERR57' in response.out

    def test_date_field_with_value_out_of_range_1(self, monkeypatch, capsys):
        # Given
        monkeypatch.setattr('sys.argv', ['pytest', '-cmd', 'cmd3'])
        TestUtil.useExecutorsInModule(['TestExecutor3'], 'test')
        self.__fieldSettings['min'] = '02-01-2021'
        TestFileUtil.saveCmdFileInCommandsDir(self.__cmdSettings, 'cmd3')
        TestFileUtil.saveArgFile({'publish_date': '01-01-2021'}, 'cmd3')
        # When
        CmdExecAppRunner.run('test')
        # Then
        response = capsys.readouterr()
        assert 'ERR56' in response.out

    def test_date_field_with_value_out_of_range_2(self, monkeypatch, capsys):
        # Given
        TestFileUtil.removeArgFile('cmd3')
        TestFileUtil.removeCmdFileFromCommandsDir('cmd3')
        monkeypatch.setattr('sys.argv', ['pytest', '-cmd', 'cmd3'])
        TestUtil.useExecutorsInModule(['TestExecutor3'], 'test')
        self.__fieldSettings['min'] = '02-01-2021'
        self.__fieldSettings['max'] = '03-01-2021'
        TestFileUtil.saveCmdFileInCommandsDir(self.__cmdSettings, 'cmd3')
        TestFileUtil.saveArgFile({'publish_date': '04-01-2021'}, 'cmd3')
        # When
        CmdExecAppRunner.run('test')
        # Then
        response = capsys.readouterr()
        assert 'ERR56' in response.out

    def test_date_field_with_invalid_formatted_value(self, monkeypatch, capsys):
        # Given
        TestFileUtil.removeArgFile('cmd3')
        TestFileUtil.removeCmdFileFromCommandsDir('cmd3')
        monkeypatch.setattr('sys.argv', ['pytest', '-cmd', 'cmd3'])
        TestUtil.useExecutorsInModule(['TestExecutor3'], 'test')
        self.__fieldSettings['format'] = '%Y'
        TestFileUtil.saveCmdFileInCommandsDir(self.__cmdSettings, 'cmd3')
        TestFileUtil.saveArgFile({'publish_date': '04-01-2021'}, 'cmd3')
        # When
        CmdExecAppRunner.run('test')
        # Then
        response = capsys.readouterr()
        assert 'ERR55' in response.out
