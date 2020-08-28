import inspect
import traceback

from app_runner.services.LogService import LogService
from app_runner.utils.StrUtil import StrUtil

class ErrorUtil:

    @staticmethod
    def raiseExceptionIfNone(obj: object, msg: str = None):
        if obj is None:
            frame = inspect.currentframe()
            caller = inspect.getouterframes(frame, 2)
            fileName: str = StrUtil.getFileNameFromPath(caller[1][1])
            fileName = StrUtil.removeFileExtension(fileName)
            methodName: str = caller[1][3]
            message: str = 'Given object is None.'
            if msg is not None:
                message = msg
            raise Exception('[{className}.{method}] {msg}'.format(className=fileName, method=methodName, msg=message))

    @staticmethod
    def handleException(exception: Exception, logService: LogService = None):
        print('\033[31mError occurred while handling request.')
        print('- Error Details:\n ' + str(exception))
        errorDetails: str = traceback.format_exc()
        if logService is not None:
            logService.error(errorDetails)
        print('- Stack Trace:\n ' + str(errorDetails) + '\033[0m')

