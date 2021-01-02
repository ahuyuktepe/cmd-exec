import os


class TestConfigUtil:

    @staticmethod
    def setTestRootPath():
        os.environ['APP_RUNNER_ROOT_PATH'] = os.environ['APP_RUNNER_ROOT_PATH'] + os.sep + 'build'
