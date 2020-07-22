import os
from app_runner.log.LogSettings import LogSettings
from app_runner.services.LogService import LogService
from app_runner.utils.FileUtil import FileUtil

class TestLogService:

    logService: LogService
    logSettings: LogSettings

    def setup(self):
        settings = {
            "dir_path": "../args",
            "level": "debug",
            "msg_format":"{level}|{msg}"
        }
        self.logSettings = LogSettings(settings)
        self.logService = LogService(settings)

    def test_write(self):
        self.setup()
        self.logService.debug('Test')
        filePath = self.logSettings.getFilePath()
        fileContent = FileUtil.readFile(filePath)
        assert fileContent.strip() == 'DEBUG   |Test'
        os.remove(filePath)

    def test_writeEmpty(self):
        self.setup()
        self.logService.warn('Test')
        filePath = self.logSettings.getFilePath()
        fileContent = FileUtil.readFile(filePath)
        assert fileContent.strip() == ''
        os.remove(filePath)


