import math
import os.path
import shutil
import yaml
from app_runner.utils.StrUtil import StrUtil

class FileUtil:
    @staticmethod
    def getAbsolutePath(path: list) -> str:
        return os.environ['APP_RUNNER_ROOT_PATH'] + os.path.sep + os.path.sep.join(path)

    @staticmethod
    def convertToPath(fileNames: list) -> str:
        return os.path.sep.join(fileNames)

    @staticmethod
    def readFile(path: str) -> str:
        if not os.path.exists(path):
            raise FileNotFoundError("File '{path}' is not found.".format(path=path))
        jsonFile = open(path)
        return jsonFile.read()

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
    def generateObjFromFile(path: str) -> object:
        fileExt: str = FileUtil.getFileExtension(path)
        if fileExt == 'json':
            return FileUtil.generateObjFromJsonFile(path)
        elif fileExt == 'yaml':
            return FileUtil.generateObjFromYamlFile(path)

    @staticmethod
    def generateObjFromJsonFile(path: str) -> object:
        jsonStr = FileUtil.readFile(path)
        return StrUtil.jsonStrToObj(jsonStr)

    @staticmethod
    def generateObjFromYamlFile(path: str) -> object:
        stream = open(path, 'r')
        return yaml.load(stream, Loader=yaml.FullLoader)

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