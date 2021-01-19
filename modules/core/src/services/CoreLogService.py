from src.config.AppConfigs import AppConfigs
from src.log.LogMessage import LogMessage
from src.log.LogSettings import LogSettings
from src.service.LogService import LogService
from src.util.FileUtil import FileUtil


class CoreLogService(LogService):
    __settings: LogSettings

    def __init__(self, appConfigs: AppConfigs):
        logConfigs = appConfigs.getValue('log_settings')
        self.__settings = LogSettings(logConfigs)

    # Getter Methods

    def getLogFilePath(self) -> str:
        return self.__settings.getFilePath()

    # Setter Methods

    def info(self, msg: str):
        self.__write(LogMessage('info',  msg))

    def debug(self, msg: str):
        self.__write(LogMessage('debug',  msg))

    def warn(self, msg: str):
        self.__write(LogMessage('warn',  msg))

    def error(self, msg: str):
        self.__write(LogMessage('error',  msg))

    # Private Methods

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
