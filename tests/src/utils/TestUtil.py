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
    def useCmdFilesInModule(cmdFileNames: list, moduleName: str):
        for fileName in cmdFileNames:
            srcFilePath = ['tests', 'test-files', 'commands', fileName]
            dstDirPath = ['tests', 'target', 'modules', moduleName, 'commands', fileName]
            TestFileUtil.copyFile(srcFilePath, dstDirPath)

    @staticmethod
    def useCmdFiles(cmdFileNames: list):
        for fileName in cmdFileNames:
            srcFilePath = ['tests', 'test-files', 'commands', fileName]
            dstDirPath = ['tests', 'target', 'resources', 'commands', fileName]
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
            srcFilePath = ['tests', 'test-files', 'services', fileName]
            dstDirPath = ['tests', 'target', 'modules', moduleName, 'src', 'service', fileName]
            TestFileUtil.copyFile(srcFilePath, dstDirPath)

    @staticmethod
    def useExecutorsInModule(execClsNames: list, moduleName: str):
        for fileName in execClsNames:
            srcFilePath = ['tests', 'test-files', 'executors', fileName]
            dstDirPath = ['tests', 'target', 'modules', moduleName, 'src', 'executor', fileName]
            TestFileUtil.copyFile(srcFilePath, dstDirPath)

    @staticmethod
    def useFieldsInModule(fieldClsNames: list, moduleName: str):
        for fileName in fieldClsNames:
            srcFilePath = ['tests', 'test-files', 'fields', fileName]
            dstDirPath = ['tests', 'target', 'modules', moduleName, 'src', 'field', fileName]
            TestFileUtil.copyFile(srcFilePath, dstDirPath)
