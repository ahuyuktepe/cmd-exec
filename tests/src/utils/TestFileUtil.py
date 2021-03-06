import os
import shutil
import yaml


class TestFileUtil:
    __rootPath: str = os.environ['APP_RUNNER_ROOT_PATH']

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
    def removeFile(path: list):
        filePath = TestFileUtil.getAbsolutePath(path)
        if os.path.exists(filePath):
            os.remove(filePath)

    @staticmethod
    def makeDir(relativePath: list):
        if not TestFileUtil.doesDirectoryExist(relativePath):
            path = TestFileUtil.getAbsolutePath(relativePath)
            os.mkdir(path)

    @staticmethod
    def makeDirs(srcDirPath: list, dirs: list):
        for dirName in dirs:
            path = srcDirPath + [dirName]
            TestFileUtil.makeDir(path)

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
    def saveCmdFileInCommandsDir(data: dict, cid: str = 'cmd'):
        path = ['tests', 'target', 'resources', 'commands', cid + '.yaml']
        TestFileUtil.saveDictAsYamlFile(data, path)

    @staticmethod
    def saveArgFile(data: dict, cid: str):
        path = ['tests', 'target', 'resources', 'arguments', cid + '.args.yaml']
        TestFileUtil.saveDictAsYamlFile(data, path)

    @staticmethod
    def saveDictAsYamlFile(data: dict, filePath: list):
        path = TestFileUtil.getAbsolutePath(filePath)
        with open(path, 'w') as file:
            yaml.dump(data, file, sort_keys= False)

    @staticmethod
    def removeArgFile(commandId: str):
        path = ['tests', 'target', 'resources', 'arguments', commandId + '.args.yaml']
        TestFileUtil.removeFile(path)

    @staticmethod
    def removeCmdFileForModule(cmdId: str, moduleId: str):
        path = ['tests', 'target', 'modules', moduleId, 'commands', cmdId + '.yaml']
        TestFileUtil.removeFile(path)

    @staticmethod
    def removeCmdFileFromCommandsDir(cmdId: str):
        path = ['tests', 'target', 'resources','commands', cmdId + '.yaml']
        TestFileUtil.removeFile(path)

    @staticmethod
    def replaceStrInFileFile(replaceStr: str, replaceWith: str, filePath: list):
        path = TestFileUtil.getAbsolutePath(filePath)
        file = open(path, 'r')
        content: str = file.read()
        file.close()
        content = content.replace(replaceStr, replaceWith)
        file = open(path, 'w')
        file.write(content)
        file.close()
