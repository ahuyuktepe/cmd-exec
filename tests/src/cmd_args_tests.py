from src.app.CmdExecAppRunner import CmdExecAppRunner
from tests.src.utils.TestFileUtil import TestFileUtil
from tests.src.utils.TestUtil import TestUtil


class TestCmdArgs:

    def setup_method(method):
        TestUtil.setupTestingEnvironment()

    def teardown_method(method):
        TestUtil.destroyTestingEnvironment()

    def testing_cmd_arg(self, monkeypatch, capsys):
        # Given
        TestUtil.useCmdFilesInModule(['cmd4'], 'core')
        TestUtil.useExecutorsInModule(['TestExecutor4'], 'core')
        # When
        monkeypatch.setattr('sys.argv', ['pytest', '-cmd', 'cmd4', '-publish_date', '01-01-2021'])
        CmdExecAppRunner.run()
        # Then
        response = capsys.readouterr()
        respStr = response.out.strip('\n')
        assert 'Running TestExecutor4' in respStr and 'publish_date=01-01-2021' in respStr

    def testing_arg_from_file(self, monkeypatch, capsys):
        # Given
        TestUtil.useCmdFilesInModule(['cmd4'], 'core')
        TestUtil.useExecutorsInModule(['TestExecutor4'], 'core')
        TestFileUtil.saveArgFile({'publish_date': '01-01-2021'}, 'cmd4')
        # When
        monkeypatch.setattr('sys.argv', ['pytest', '-cmd', 'cmd4'])
        CmdExecAppRunner.run()
        # Then
        response = capsys.readouterr()
        respStr = response.out.strip('\n')
        assert 'Running TestExecutor4' in respStr and 'publish_date=01-01-2021' in respStr

    def testing_cmd_from_commands_directory(self, monkeypatch, capsys):
        # Given
        TestFileUtil.removeCmdFileFromCommandsDir('cmd4')
        TestUtil.useCmdFilesInCommandsDir(['cmd4'])
        TestUtil.useExecutorsInModule(['TestExecutor4'], 'core')
        # When
        monkeypatch.setattr('sys.argv', ['pytest', '-cmd', 'cmd4', '-publish_date', '01-01-2021'])
        CmdExecAppRunner.run()
        # Then
        response = capsys.readouterr()
        respStr = response.out.strip('\n')
        assert 'Running TestExecutor4' in respStr and 'publish_date=01-01-2021' in respStr
