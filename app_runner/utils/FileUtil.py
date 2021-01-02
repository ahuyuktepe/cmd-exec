import math
import os.path
import shutil
import yaml
from app_runner.errors.AppRunnerError import AppRunnerError
from app_runner.utils.StrUtil import StrUtil
import xml.etree.ElementTree as ET


class FileUtil:

    @staticmethod
    def generateObjFromFile(path: str) -> object:
        fileExt: str = FileUtil.getFileExtension(path)
        if fileExt == 'json':
            return FileUtil.generateObjFromJsonFile(path)
        elif fileExt == 'yaml':
            return FileUtil.generateObjFromYamlFile(path)
        elif fileExt == 'xml':
            return FileUtil.generateObjFromXmlFile(path)

    @staticmethod
    def generateObjFromYamlFile(path: str) -> object:
        try:
            stream = open(path, 'r')
            retObj = yaml.load(stream, Loader=yaml.SafeLoader)
            return retObj
        except Exception as exp:
            msg = "Error occurred while parsing xml file '{path}'.".format(path=path)
            raise AppRunnerError(msg)

    @staticmethod
    def generateObjFromXmlFile(path: str) -> object:
        try:
            tree = ET.parse(path)
            return tree
        except Exception as exp:
            msg = "Error occurred while parsing xml file '{path}'.".format(path= path)
            raise AppRunnerError(msg)

    @staticmethod
    def generateObjFromJsonFile(path: str) -> object:
        try:
            jsonStr = FileUtil.readFile(path)
            return StrUtil.jsonStrToObj(jsonStr)
        except Exception as exp:
            msg = "Error occurred while parsing json file '{path}'.".format(path=path)
            raise AppRunnerError(msg)

    @staticmethod
    def isFileReadable(filePath: str):
        return not FileUtil.isDirectory(filePath) and FileUtil.doesFileExist(filePath) and FileUtil.doesUserHaveAccessOnFile(filePath)

    # ==============================================================================================================

    @staticmethod
    def getAbsolutePath(path: list) -> str:
        return os.environ['APP_RUNNER_ROOT_PATH'] + os.path.sep + os.path.sep.join(path)

    @staticmethod
    def readFile(path: str) -> str:
        jsonFile = open(path)
        return jsonFile.read()

    @staticmethod
    def failIfClassFileDoesNotExist(mid: str, cls: str, dirName: str):
        if mid is not None:
            filePath: str = FileUtil.getAbsolutePath(['modules', mid, 'src', dirName, cls + '.py'])

    @staticmethod
    def convertToPath(fileNames: list) -> str:
        return os.path.sep.join(fileNames)

    @staticmethod
    def writeFile(path: str, content: str):
        file = open(path, 'w')
        file.write(content)
        file.close()

    @staticmethod
    def copyFile(sourceFilePath: str, destFilePath: str):
        shutil.copy(sourceFilePath, destFilePath)

    @staticmethod
    def deleteFile(path: str):
        if FileUtil.doesFileExist(path) and FileUtil.isFile(path):
            os.remove(path)

    @staticmethod
    def deleteFilesInDir(dirPath: str, fileNames: list):
        for fileName in fileNames:
            filePath = dirPath + os.path.sep + fileName
            if FileUtil.isFile(filePath) and FileUtil.doesFileExist(filePath):
                FileUtil.deleteFile(filePath)

    @staticmethod
    def doesFileExist(path: str) -> bool:
        return os.path.exists(path)

    @staticmethod
    def doesDirExist(path: str) -> bool:
        return os.path.exists(path)

    @staticmethod
    def fileSize(path: str, blockSize: str) -> int:
        fileStats = os.stat(path)
        if blockSize == 'MB':
            return math.floor(fileStats.st_size / (1024 * 1024))
        elif blockSize == 'KB':
            return math.floor(fileStats.st_size/1024)
        return fileStats.st_size

    @staticmethod
    def getFileExtension(filePath: str) -> str:
        return filePath.split('.')[-1]

    @staticmethod
    def isFile(path: str) -> bool:
        return os.path.isfile(path)
    @staticmethod
    def isDirectory(path: str) -> bool:
        return os.path.isdir(path)

    @staticmethod
    def saveObjIntoFileAsYaml(path: str, data: object):
        content: str = yaml.safe_dump(data)
        FileUtil.writeFile(path, content)

    @staticmethod
    def doesUserHaveAccessOnFile(filePath: str) -> bool:
        return os.access(filePath, os.R_OK)

    @staticmethod
    def getServiceClassFilePath(module: str, cls: str) -> str:
        return FileUtil.getAbsolutePath(['modules', module, 'src', 'services', cls])

    @staticmethod
    def makeDir(dirPath: str):
        os.mkdir(dirPath)

    @staticmethod
    def makeDirsInSrcDir(srcDirPath: str, dirs: list):
        if FileUtil.isDirectory(srcDirPath) and FileUtil.doesDirExist(srcDirPath):
            dirPath = srcDirPath
            for dir in dirs:
                dirPath = dirPath + os.sep + dir
                if not FileUtil.doesDirExist(dirPath):
                    FileUtil.makeDir(dirPath)


