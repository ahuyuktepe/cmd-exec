import math
import os.path
import shutil
import yaml
from classes.utils.StrUtil import StrUtil

class FileUtil:
    @staticmethod
    def readFileContent(path: str) -> str:
        if not os.path.exists(path):
            raise FileNotFoundError("File '{path}' is not found.".format(path=path))
        jsonFile = open(path)
        return jsonFile.read()

    @staticmethod
    def generateObjFromJsonFile(path: str) -> object:
        jsonStr = FileUtil.readFileContent(path)
        return StrUtil.jsonStrToObj(jsonStr)

    @staticmethod
    def generateObjFromYamlFile(path: str) -> object:
        stream = open(path, 'r')
        return yaml.load(stream, Loader=yaml.FullLoader)

    @staticmethod
    def doesFileExist(path: str) -> bool:
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
    def copyFile(sourceFilePath: str, destFilePath: str):
        shutil.copy(sourceFilePath, destFilePath)

    @staticmethod
    def getMenuFilePath(mid: str):
        return 'menus/{mid}-menu.yaml'.format(mid=mid)
