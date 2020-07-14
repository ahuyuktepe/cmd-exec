import inspect
from classes.utils.StrUtil import StrUtil

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
