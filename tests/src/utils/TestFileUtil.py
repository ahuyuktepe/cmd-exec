import os
import shutil

import yaml

from src.error.CmdExecError import CmdExecError


class TestFileUtil:
    __rootPath: str = None
    __isInitialized: bool = False

    @staticmethod
    def initialize(path: str = None):
        if not TestFileUtil.__isInitialized:
            pathEnv = os.environ['APP_RUNNER_ROOT_PATH']
            if path is not None:
                TestFileUtil.__rootPath = path
            elif pathEnv is None:
                TestFileUtil.__rootPath = os.path.abspath('')
            else:
                TestFileUtil.__rootPath = pathEnv
            TestFileUtil.__isInitialized = True

    @staticmethod
    def doesDirectoryExist(relativePath: list) -> bool:
        path = TestFileUtil.getAbsolutePath(relativePath)
        return os.path.exists(path)

    @staticmethod
    def listFiles(relativePath: list) -> list:
        path = TestFileUtil.getAbsolutePath(relativePath)
        return os.listdir(path)

    @staticmethod
    def copyDirectory(srcPath: list, destPath: list):
        srcDirPath = TestFileUtil.getAbsolutePath(srcPath)
        destDirPath = TestFileUtil.getAbsolutePath(destPath)
        shutil.copytree(srcDirPath, destDirPath)

    @staticmethod
    def copyFile(srcPath: list, destPath: list):
        srcDirPath = TestFileUtil.getAbsolutePath(srcPath)
        destDirPath = TestFileUtil.getAbsolutePath(destPath)
        shutil.copy(srcDirPath, destDirPath)

    @staticmethod
    def makeDir(relativePath: list):
        if not TestFileUtil.doesDirectoryExist(relativePath):
            path = TestFileUtil.getAbsolutePath(relativePath)
            os.mkdir(path)

    @staticmethod
    def deleteDir(relativePath: list):
        if isinstance(relativePath, list) and relativePath:
            dirName = relativePath[-1]
            if dirName not in ['.', '..'] and TestFileUtil.doesDirectoryExist(relativePath):
                srcPath = TestFileUtil.getAbsolutePath(relativePath)
                shutil.rmtree(srcPath)

    @staticmethod
    def getAbsolutePath(relativePath: list) -> str:
        return TestFileUtil.__rootPath + os.path.sep + os.path.sep.join(relativePath)

    @staticmethod
    def saveCmdFileForModule(data: dict, commandId: str, moduleId: str):
        path = ['tests', 'target', 'modules', moduleId, 'commands', commandId + '.yaml']
        TestFileUtil.saveDictAsYamlFile(data, path)

    @staticmethod
    def saveCmdFileInCommandsDir(data: dict, commandId: str, moduleId: str):
        path = ['tests', 'target', 'resources', 'commands', commandId + '.yaml']
        TestFileUtil.saveDictAsYamlFile(data, path)

    @staticmethod
    def saveArgFile(data: dict, commandId: str):
        path = ['tests', 'target', 'resources', 'arguments', commandId + '.args.yaml']
        TestFileUtil.saveDictAsYamlFile(data, path)

    @staticmethod
    def saveDictAsYamlFile(data: dict, filePath: list):
        path = TestFileUtil.getAbsolutePath(filePath)
        with open(path, 'w') as file:
            yaml.dump(data, file, sort_keys= False)
