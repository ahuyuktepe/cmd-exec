from src.util.FileUtil import FileUtil
from tests.utils.TestFileUtil import TestFileUtil


class TestModuleUtil:

    @staticmethod
    def generateModulesDir():
        dirPath = FileUtil.getAbsolutePath(['modules'])
        FileUtil.makeDir(dirPath)

    @staticmethod
    def generateModuleDir(name: str):
        dirPath = FileUtil.getAbsolutePath(['modules', name])
        FileUtil.makeDir(dirPath)

    @staticmethod
    def generateSettingsFile(name: str, settings: dict):
        if settings is not None:
            settingsFileName = name + '.settings.yaml'
            filePath = FileUtil.getAbsolutePath(['modules', name, settingsFileName])
            TestFileUtil.saveObjIntoFileAsYaml(filePath, settings)

    @staticmethod
    def generateConfigsFile(name: str, settings: dict):
        if settings is not None:
            configsFileName = name + '.config.yaml'
            filePath = FileUtil.getAbsolutePath(['modules', name, configsFileName])
            TestFileUtil.saveObjIntoFileAsYaml(filePath, settings)
