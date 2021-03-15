from src.app.CmdExecAppRunner import CmdExecAppRunner
from tests.src.utils.TestFileUtil import TestFileUtil
from tests.src.utils.TestUtil import TestUtil


class TestCmdArgs:

    def setup_method(method):
        TestUtil.setupTestingEnvironment()

    def teardown_method(method):
        # TestUtil.destroyTestingEnvironment()
        pass

    def testing_cmd_arg(self, monkeypatch, capsys):
        # Given
        TestUtil.buildModuleFiles('test', {
            'name': 'test',
            'version': '0.0.1'
        })
        TestUtil.useConfigFilesInConfigsDir(['main.config.yaml'])
        TestUtil.useCmdFilesInCommandsDir(['cmd4'])
        TestUtil.useExecutorsInModule(['TestExecutor4'], 'test')
        # When
        monkeypatch.setattr('sys.argv', ['pytest', '-cmd', 'test.cmd4', '-publish_date', '01-01-2021'])
        CmdExecAppRunner.run()
        # Then
        response = capsys.readouterr()
        respStr = response.out.strip('\n')
        assert 'Running TestExecutor4' in respStr and 'publish_date=01-01-2021' in respStr

    def testing_arg_from_file(self, monkeypatch, capsys):
        # Given
        TestUtil.buildModuleFiles('test', {
            'name': 'test',
            'version': '0.0.1'
        })
        TestUtil.useConfigFilesInConfigsDir(['main.config.yaml'])
        TestUtil.useCmdFilesInModule(['cmd4'], 'test')
        TestUtil.useExecutorsInModule(['TestExecutor4'], 'test')
        TestFileUtil.saveArgFile({'publish_date': '01-01-2021'}, 'cmd4')
        # When
        monkeypatch.setattr('sys.argv', ['pytest', '-cmd', 'test.cmd4'])
        CmdExecAppRunner.run()
        # Then
        response = capsys.readouterr()
        respStr = response.out.strip('\n')
        assert 'Running TestExecutor4' in respStr and 'publish_date=01-01-2021' in respStr

    def testing_cmd_from_commands_directory(self, monkeypatch, capsys):
        # Given
        TestUtil.buildModuleFiles('test', {
            'name': 'test',
            'version': '0.0.1'
        })
        TestUtil.useConfigFilesInConfigsDir(['main.config.yaml'])
        TestFileUtil.removeCmdFileFromCommandsDir('cmd4')
        TestUtil.useCmdFilesInCommandsDir(['cmd4'])
        TestUtil.useExecutorsInModule(['TestExecutor4'], 'test')
        # When
        monkeypatch.setattr('sys.argv', ['pytest', '-cmd', 'test.cmd4', '-publish_date', '01-01-2021'])
        CmdExecAppRunner.run()
        # Then
        response = capsys.readouterr()
        respStr = response.out.strip('\n')
        assert 'Running TestExecutor4' in respStr and 'publish_date=01-01-2021' in respStr
