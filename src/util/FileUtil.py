import os
import shutil
import yaml
from src.error.CmdExecError import CmdExecError


class FileUtil:
    __rootPath: str = os.environ['APP_RUNNER_ROOT_PATH']

    @staticmethod
    def getAbsolutePath(relativePath: list) -> str:
        return FileUtil.__rootPath + os.path.sep + os.path.sep.join(relativePath)

    @staticmethod
    def generateObjFromYamlFile(relativePath: list) -> dict:
        path = FileUtil.getAbsolutePath(relativePath)
        try:
            stream = open(path, 'r')
            retObj = yaml.load(stream, Loader=yaml.SafeLoader)
            return retObj
        except Exception as exp:
            msg = "Error occurred while parsing xml file '{path}'.".format(path=path)
            raise CmdExecError(msg)

    # Query Methods

    @staticmethod
    def isDirectoryReadable(relativePath: list):
        return FileUtil.isDirectory(relativePath) and FileUtil.doesFileExist(relativePath) and FileUtil.doesUserHaveAccessOnFile(relativePath)

    @staticmethod
    def isFileReadable(relativePath: list):
        return not FileUtil.isDirectory(relativePath) and FileUtil.doesFileExist(relativePath) and FileUtil.doesUserHaveAccessOnFile(relativePath)

    @staticmethod
    def isDirectory(relativePath: list) -> bool:
        path = FileUtil.getAbsolutePath(relativePath)
        return os.path.isdir(path)

    @staticmethod
    def doesFileExist(relativePath: list) -> bool:
        path = FileUtil.getAbsolutePath(relativePath)
        return os.path.exists(path)

    @staticmethod
    def doesUserHaveAccessOnFile(relativePath: list) -> bool:
        path = FileUtil.getAbsolutePath(relativePath)
        return os.access(path, os.R_OK)

    # Directory or File Updating Commands

    @staticmethod
    def makeDir(relativePath: list):
        if not FileUtil.doesFileExist(relativePath):
            path = FileUtil.getAbsolutePath(relativePath)
            os.mkdir(path)

    @staticmethod
    def deleteDir(relativePath: list):
        ignoredDirs = ['src', 'logs', 'temp', 'modules', 'app_runner']
        dirName = relativePath[-1]
        if dirName in ignoredDirs:
            raise CmdExecError('ERR21', {'dirs': str(ignoredDirs), 'home': FileUtil.__rootPath})
        if relativePath != [] and FileUtil.isDirectory(relativePath) and FileUtil.doesFileExist(relativePath) and dirName not in ignoredDirs:
            srcPath = FileUtil.getAbsolutePath(relativePath)
            shutil.rmtree(srcPath)

    @staticmethod
    def writeToFile(relativePath: list, content: str):
        path = FileUtil.getAbsolutePath(relativePath)
        file = open(path, 'w')
        file.write(content)
        file.close()

    # ==================================================================================================================

    # @staticmethod
    # def fileSize(path: str, blockSize: str) -> int:
    #     fileStats = os.stat(path)
    #     if blockSize == 'MB':
    #         return math.floor(fileStats.st_size / (1024 * 1024))
    #     elif blockSize == 'KB':
    #         return math.floor(fileStats.st_size/1024)
    #     return fileStats.st_size
    #
    # @staticmethod
    # def copyFile(sourceFilePath: str, destFilePath: str):
    #     shutil.copy(sourceFilePath, destFilePath)
    #
    # @staticmethod
    # def makeDir(dirPath: str):
    #     if not FileUtil.doesFileExist(dirPath):
    #         os.mkdir(dirPath)
    #
    # @staticmethod
    # def isFile(path: str) -> bool:
    #     return os.path.isfile(path)
