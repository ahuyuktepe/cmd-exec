from cmd_exec.app.CmdExecAppRunner import CmdExecAppRunner
from tests.src.utils.TestFileUtil import TestFileUtil
from tests.src.utils.TestUtil import TestUtil


class TestConstraints:
    def setup_method(method):
        TestUtil.setupTestingEnvironment()
        TestUtil.buildModuleFiles('test', {
            'name': 'test',
            'version': '0.0.1'
        })

    def teardown_method(method):
        TestUtil.destroyTestingEnvironment()

    def testingAllowedUsers(self, monkeypatch, capsys):
        TestUtil.useCmdFilesInCommandsDir(['cmd11'])
        TestUtil.useExecutorsInModule(['TestExecutor1'], 'test')
        # Given
        monkeypatch.setattr('sys.argv', ['pytest', '-cmd', 'cmd11'])
        # When
        CmdExecAppRunner.run('test')
        # Then
        response = capsys.readouterr()
        assert 'ERR78' in response.out

    def testingDeniedUsers(self, monkeypatch, capsys):
        TestUtil.useCmdFilesInCommandsDir(['cmd12'])
        TestFileUtil.replaceStrInFileFile('USER_NAME', 'test_user', ['tests', 'target', 'resources', 'commands', 'cmd12.yaml'])
        TestUtil.useExecutorsInModule(['TestExecutor1'], 'test')
        # Given
        monkeypatch.setattr('sys.argv', ['pytest', '-cmd', 'cmd12'])
        # When
        CmdExecAppRunner.run('test')
        # Then
        response = capsys.readouterr()
        assert 'ERR78' in response.out
