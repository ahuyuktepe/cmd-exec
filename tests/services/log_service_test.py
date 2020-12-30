import os
from app_runner.log.LogSettings import LogSettings
from app_runner.services.LogService import LogService
from app_runner.utils.FileUtil import FileUtil

class TestLogService:

    logService: LogService
    logSettings: LogSettings

    def setup(self, settings: dict = None):
        if settings is None:
            settings = {
                "dir_path": "temp",
                "level": "debug",
                "msg_format": "{level}|{msg}",
                "max_size": "1 B"
            }
        self.logSettings = LogSettings(settings)
        self.logService = LogService(settings)

    def test_write(self):
        # given
        self.setup()
        # when
        self.logService.debug('Test')
        # then
        filePath = self.logSettings.getFilePath()
        fileContent = FileUtil.readFile(filePath)
        assert fileContent.strip() == 'DEBUG   |Test'
        os.remove(filePath)

    def test_writeEmpty(self):
        # given
        self.setup()
        # when
        self.logService.warn('Test')
        # then
        filePath = self.logSettings.getFilePath()
        fileContent = FileUtil.readFile(filePath)
        assert fileContent.strip() == 'WARN    |Test'
        os.remove(filePath)

    def test_logFileBackup(self):
        # given
        self.setup()
        tempDirPath = FileUtil.getAbsolutePath(['temp'])
        FileUtil.deleteFilesInDir(tempDirPath, ['core.log', 'main_1.log'])
        # when
        self.logService.warn('Initial log message. Please ignore.')
        # then
        logFilePath = FileUtil.convertToPath([tempDirPath, 'core.log'])
        mainFileExist: bool = FileUtil.doesFileExist(logFilePath)
        # when
        self.logService.warn('Second log message. Please ignore.')
        # then
        logFilePath = FileUtil.convertToPath([tempDirPath, 'main_1.log'])
        assert mainFileExist and FileUtil.doesFileExist(logFilePath)
        FileUtil.deleteFilesInDir(tempDirPath, ['core.log', 'main_1.log'])