from classes.utils.FileUtil import FileUtil


class LogSettings:
    _level: str = 'info'
    _dirPath: str = 'logs'
    _fileName: str = 'main'
    _maxSize: str = '1 B'
    _msgFormat: str = '{level} : {msg}'
    _dateFormat: str = '%Y-%m-%d %H:%M:%S'

    def __init__(self, values: dict):
        if values is not None:
            if values.get('level') is not None:
                self._level = values.get('level')
            if values.get('dir_path') is not None:
                self._dirPath = values.get('dir_path')
            if values.get('max_size') is not None:
                self._maxSize = values.get('max_size')
            if values.get('file_name') is not None:
                self._fileName = values.get('file_name')
            if values.get('msg_format') is not None:
                self._msgFormat = values.get('msg_format')
            if values.get('date_format') is not None:
                self._dateFormat = values.get('date_format')

    def getLevel(self) -> str:
        return self._level

    def getMsgFormat(self) -> str:
        return self._msgFormat

    def getDateFormat(self) -> str:
        return self._dateFormat

    def getFilePath(self, version: int = None):
        return "{dirPath}/{fileName}.log".format(dirPath=self._dirPath, fileName=self._fileName)

    def getVersionFilePath(self, version: int):
        return "{dirPath}/{fileName}_{version}.log".format(dirPath=self._dirPath, fileName=self._fileName, version=version)

    def getMaxSizeBlockSize(self) -> str:
        arr: list = self._maxSize.split(' ')
        return arr[1]

    def getMaxSize(self) -> int:
        arr: list = self._maxSize.split(' ')
        return int(arr[0])
