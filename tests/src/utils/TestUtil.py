import os

from src.util.FileUtil import FileUtil
from src.util.ObjUtil import ObjUtil
from tests.src.utils.TestFileUtil import TestFileUtil


class TestUtil:

    @staticmethod
    def setupTestingEnvironment():
        ObjUtil.setEnvironment('test')
        path = os.path.abspath('../target')
        FileUtil.initialize(path)
        path = os.path.abspath('../..')
        TestFileUtil.initialize(path)
        TestUtil.__clearTargetDirectory()
        TestUtil.__copyModules()
        TestUtil.__buildResourcesDirectory()

    @staticmethod
    def destroyTestingEnvironment():
        TestUtil.__clearTargetDirectory()

    @staticmethod
    def __clearTargetDirectory():
        path = ['tests', 'target']
        if TestFileUtil.doesDirectoryExist(path):
            dirs = TestFileUtil.listFiles(path)
            for dirName in dirs:
                TestFileUtil.deleteDir(['tests', 'target', dirName])

    @staticmethod
    def __copyModules():
        if TestFileUtil.doesDirectoryExist(['modules']):
            dirs = TestFileUtil.listFiles(['modules'])
            for srcDir in dirs:
                srcPath = ['modules', srcDir]
                TestFileUtil.makeDir(srcPath)
                TestFileUtil.copyDirectory(srcPath, ['tests', 'target', 'modules', srcDir])

    @staticmethod
    def __buildResourcesDirectory():
        path = ['tests', 'target', 'resources']
        TestFileUtil.deleteDir(path)
        TestFileUtil.makeDir(path)
        path = ['tests', 'target', 'resources', 'arguments']
        TestFileUtil.makeDir(path)
        path = ['tests', 'target', 'resources', 'commands']
        TestFileUtil.makeDir(path)

    @staticmethod
    def useCmdFilesInModule(cmdFileNames: list, moduleName: str = 'core'):
        for fileName in cmdFileNames:
            srcFilePath = ['tests', 'test-files', 'commands', fileName + '.yaml']
            dstDirPath = ['tests', 'target', 'modules', moduleName, 'commands', fileName + '.yaml']
            TestFileUtil.copyFile(srcFilePath, dstDirPath)

    @staticmethod
    def useCmdFilesInCommandsDir(cmdFileNames: list):
        for fileName in cmdFileNames:
            srcFilePath = ['tests', 'test-files', 'commands', fileName + '.yaml']
            dstDirPath = ['tests', 'target', 'resources', 'commands', fileName + '.yaml']
            TestFileUtil.copyFile(srcFilePath, dstDirPath)

    @staticmethod
    def useArgFiles(argFileNames: list):
        for fileName in argFileNames:
            srcFilePath = ['tests', 'test-files', 'arguments', fileName]
            dstDirPath = ['tests', 'target', 'resources', 'arguments', fileName]
            TestFileUtil.copyFile(srcFilePath, dstDirPath)

    @staticmethod
    def useServicesInModule(srvClsNames: list, moduleName: str):
        for fileName in srvClsNames:
            srcFilePath = ['tests', 'test-files', 'services', fileName + '.py']
            dstDirPath = ['tests', 'target', 'modules', moduleName, 'src', 'service', fileName + '.py']
            TestFileUtil.copyFile(srcFilePath, dstDirPath)

    @staticmethod
    def useExecutorsInModule(execClsNames: list, moduleName: str = 'core'):
        for fileName in execClsNames:
            srcFilePath = ['tests', 'test-files', 'executors', fileName + '.py']
            dstDirPath = ['tests', 'target', 'modules', moduleName, 'src', 'executor', fileName + '.py']
            TestFileUtil.copyFile(srcFilePath, dstDirPath)

    @staticmethod
    def useExecutorInModuleAsInGivenName(srcClsName: str, destClsName: str, moduleName: str = 'core'):
        srcFilePath = ['tests', 'test-files', 'executors', srcClsName + '.py']
        dstDirPath = ['tests', 'target', 'modules', moduleName, 'src', 'executor', destClsName + '.py']
        TestFileUtil.copyFile(srcFilePath, dstDirPath)

    @staticmethod
    def useCmdAppInModuleAsInGivenName(srcClsName: str, destClsName: str, moduleName: str = 'core'):
        srcFilePath = ['tests', 'test-files', 'app', srcClsName + '.py']
        dstDirPath = ['tests', 'target', 'modules', moduleName, 'src', 'app', destClsName + '.py']
        TestFileUtil.copyFile(srcFilePath, dstDirPath)

    @staticmethod
    def useFieldsInModule(fieldClsNames: list, moduleName: str = 'core'):
        for fileName in fieldClsNames:
            srcFilePath = ['tests', 'test-files', 'fields', fileName]
            dstDirPath = ['tests', 'target', 'modules', moduleName, 'src', 'field', fileName]
            TestFileUtil.copyFile(srcFilePath, dstDirPath)

    @staticmethod
    def useProvidersInModule(providers: list, moduleName: str = 'core'):
        for fileName in providers:
            srcFilePath = ['tests', 'test-files', 'providers', fileName + '.py']
            dstDirPath = ['tests', 'target', 'modules', moduleName, 'src', 'provider', fileName + '.py']
            TestFileUtil.copyFile(srcFilePath, dstDirPath)

    @staticmethod
    def buildModuleFiles(name: str, settings: dict = {}, config: dict = {}):
        # Generating Module Directories
        path = ['tests', 'target', 'modules', name]
        TestFileUtil.makeDir(path)
        srcPath = path + ['src']
        TestFileUtil.makeDir(srcPath)
        TestFileUtil.makeDirs(srcPath, ['app', 'executor', 'field', 'service'])
        # Saving Settings File
        settingsFilePath = ['tests', 'target', 'modules', name, (name + '.settings.yaml')]
        TestFileUtil.saveDictAsYamlFile(settings, settingsFilePath)
        # Saving Config File
        configFilePath = ['tests', 'target', 'modules', name, (name + '.config.yaml')]
        TestFileUtil.saveDictAsYamlFile(config, configFilePath)
