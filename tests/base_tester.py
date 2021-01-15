import os
from src.util.FileUtil import FileUtil
from tests.utils.TestModuleUtil import TestModuleUtil


class TestBase:

    def prepareForTest(self):
        dirPath = os.environ['APP_RUNNER_ROOT_PATH']
        FileUtil.makeDir(dirPath)
        # Generate Modules Directory
        TestModuleUtil.generateModulesDir()
