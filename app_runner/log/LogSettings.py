from app_runner.utils.DataUtil import DataUtil
from app_runner.utils.FileUtil import FileUtil


class LogSettings:
    _level: str
    _dirPath: str
    _fileName: str
    _maxSize: str
    _msgFormat: str
    _dateFormat: str

    def __init__(self, values: dict):
        if values is not None:
            self._level = DataUtil.getDefaultIfNone(values.get('level'), 'info')
            self._dirPath = DataUtil.getDefaultIfNone(values.get('dir_path'), 'logs')
            self._fileName = DataUtil.getDefaultIfNone(values.get('file_name'), 'main')
            self._maxSize = DataUtil.getDefaultIfNone(values.get('max_size'), '1 MB')
            self._msgFormat = DataUtil.getDefaultIfNone(values.get('msg_format'), '{level} : {msg}')
            self._dateFormat = DataUtil.getDefaultIfNone(values.get('date_format'), '%Y-%m-%d %H:%M:%S')

    def getLevel(self) -> str:
        return self._level

    def getMsgFormat(self) -> str:
        return self._msgFormat

    def getDateFormat(self) -> str:
        return self._dateFormat

    def getFilePath(self, version: int = None):
        path = FileUtil.getAbsolutePath(['{dirPath}', '{fileName}.log'])
        return path.format(dirPath=self._dirPath, fileName=self._fileName)

    def getVersionFilePath(self, version: int):
        path = FileUtil.getAbsolutePath(['{dirPath}', '{fileName}_{version}.log'])
        return path.format(dirPath=self._dirPath, fileName=self._fileName, version=version)

    def getMaxSizeBlockSize(self) -> str:
        arr: list = self._maxSize.split(' ')
        return arr[1]

    def getMaxSize(self) -> int:
        arr: list = self._maxSize.split(' ')
        return int(arr[0])
