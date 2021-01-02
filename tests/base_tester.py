import os
from src.util.FileUtil import FileUtil
from tests.utils.TestConfigUtil import TestConfigUtil
from tests.utils.TestModuleUtil import TestModuleUtil


class TestBase:

    def prepareForTest(self):
        # given
        TestConfigUtil.setTestRootPath()
        dirPath = os.environ['APP_RUNNER_ROOT_PATH']
        FileUtil.makeDir(dirPath)
        # Generate Modules Directory
        TestModuleUtil.generateModulesDir()
