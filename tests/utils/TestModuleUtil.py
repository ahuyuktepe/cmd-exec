import os
from src.util.FileUtil import FileUtil
from tests.utils.TestFileUtil import TestFileUtil


class TestModuleUtil:

    @staticmethod
    def generateModulesDir():
        dirPath = FileUtil.getAbsolutePath(['modules'])
        FileUtil.makeDir(dirPath)

    @staticmethod
    def generateModuleFiles(name: str, config: dict, settings: dict):
        dirPath = FileUtil.getAbsolutePath(['modules', name])
        FileUtil.makeDir(dirPath)
        # Save Configs
        TestFileUtil.saveObjIntoFileAsYaml(dirPath, config)
        # Save Settings
        TestFileUtil.saveObjIntoFileAsYaml(dirPath, settings)
