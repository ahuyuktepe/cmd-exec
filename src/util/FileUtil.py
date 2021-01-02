import math
import os
import shutil
import yaml
import glob
from src.error.CmdExecError import CmdExecError


class FileUtil:
    @staticmethod
    def getAbsolutePath(path: list) -> str:
        return os.environ['APP_RUNNER_ROOT_PATH'] + os.path.sep + os.path.sep.join(path)

    @staticmethod
    def generateObjFromYamlFile(path: str) -> dict:
        try:
            stream = open(path, 'r')
            retObj = yaml.load(stream, Loader=yaml.SafeLoader)
            return retObj
        except Exception as exp:
            msg = "Error occurred while parsing xml file '{path}'.".format(path=path)
            raise CmdExecError(msg)

    @staticmethod
    def getModuleConfigFilePaths() -> list:
        modulesDirPath = FileUtil.getAbsolutePath(['modules'])
        filePattern = "{modulesDirPath}/*/*.config.yaml".format(modulesDirPath=modulesDirPath)
        return glob.glob(filePattern)

    @staticmethod
    def getModuleSettingFilePaths() -> list:
        modulesDirPath = FileUtil.getAbsolutePath(['modules'])
        filePattern = "{modulesDirPath}/*/*.settings.yaml".format(modulesDirPath=modulesDirPath)
        return glob.glob(filePattern)

    @staticmethod
    def isFileReadable(filePath: str):
        return not FileUtil.isDirectory(filePath) and FileUtil.doesFileExist(filePath) and FileUtil.doesUserHaveAccessOnFile(filePath)

    @staticmethod
    def isDirectory(path: str) -> bool:
        return os.path.isdir(path)

    @staticmethod
    def doesFileExist(path: str) -> bool:
        return os.path.exists(path)

    @staticmethod
    def doesUserHaveAccessOnFile(filePath: str) -> bool:
        return os.access(filePath, os.R_OK)

    @staticmethod
    def fileSize(path: str, blockSize: str) -> int:
        fileStats = os.stat(path)
        if blockSize == 'MB':
            return math.floor(fileStats.st_size / (1024 * 1024))
        elif blockSize == 'KB':
            return math.floor(fileStats.st_size/1024)
        return fileStats.st_size

    @staticmethod
    def copyFile(sourceFilePath: str, destFilePath: str):
        shutil.copy(sourceFilePath, destFilePath)

    @staticmethod
    def makeDir(dirPath: str):
        if not FileUtil.doesFileExist(dirPath):
            os.mkdir(dirPath)
