import os
from classes.log.LogSettings import LogSettings
from classes.services.LogService import LogService
from classes.utils.FileUtil import FileUtil

class TestLogService:

    logService: LogService
    logSettings: LogSettings

    def setup(self):
        settings = {
            "dir_path": "../temp",
            "level": "debug",
            "msg_format":"{level}|{msg}"
        }
        self.logSettings = LogSettings(settings)
        self.logService = LogService(settings)

    def test_write(self):
        self.setup()
        self.logService.debug('Test')
        filePath = self.logSettings.getFilePath()
        fileContent = FileUtil.readFileContent(filePath)
        assert fileContent.strip() == 'DEBUG   |Test'
        os.remove(filePath)

    def test_writeEmpty(self):
        self.setup()
        self.logService.warn('Test')
        filePath = self.logSettings.getFilePath()
        fileContent = FileUtil.readFileContent(filePath)
        assert fileContent.strip() == ''
        os.remove(filePath)


