from app_runner.log.LogMessage import LogMessage
from app_runner.log.LogSettings import LogSettings
from app_runner.utils.FileUtil import FileUtil

class LogService:
    __settings: LogSettings

    def __init__(self, obj: dict):
        self.__settings = LogSettings(obj)

    def __write(self, logMsg: LogMessage):
        file = open(self.__settings.getFilePath(), 'a')
        logLevel: str = self.__settings.getLevel()
        if logMsg.isLevel(logLevel):
            self.__backupFileIfLarge()
            formattedMsg = logMsg.getFormattedMessage(self.__settings)
            file.write(formattedMsg)
            file.close()

    def __backupFileIfLarge(self):
        blockSize = self.__settings.getMaxSizeBlockSize()
        targetFileSize = self.__settings.getMaxSize()
        fileSize = FileUtil.fileSize(self.__settings.getFilePath(), blockSize)
        if fileSize >= targetFileSize:
            backupFilePath = self.__getBackupFileName()
            srcFilePath = self.__settings.getFilePath()
            FileUtil.copyFile(srcFilePath, backupFilePath)
            self.__clearLogs()

    def info(self, msg: str):
        self.__write(LogMessage('info',  msg))

    def debug(self, msg: str):
        self.__write(LogMessage('debug',  msg))

    def warn(self, msg: str):
        self.__write(LogMessage('warn',  msg))

    def error(self, msg: str):
        self.__write(LogMessage('error',  msg))

    def __getBackupFileName(self) -> str:
        version = 1
        filePath = self.__settings.getVersionFilePath(version)
        while FileUtil.doesFileExist(filePath):
            version = version + 1
            filePath = self.__settings.getVersionFilePath(version)
        return filePath

    def __clearLogs(self):
        file = open(self.__settings.getFilePath(), 'r+')
        file.truncate()
        file.close()
