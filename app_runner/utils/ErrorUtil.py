import traceback
from app_runner.errors.AppRunnerError import AppRunnerError
from app_runner.services.LogService import LogService

class ErrorUtil:

    @staticmethod
    def handleException(exception: Exception, logService: LogService = None):
        if isinstance(exception, AppRunnerError):
            print('Error occurred while running application.')
            print('\nError Details:\n' + str(exception))
            errorDetails: str = traceback.format_exc()
            if logService is not None:
                logService.error(errorDetails)
                logFilePath = logService.getLogFilePath()
                print("\nFor More Information:\n" + logFilePath)
            else:
                print('\nStack Trace:\n ' + str(errorDetails))
        else:
            print('Unknown error occurred.')
            print('\nError Details:\n ' + str(exception))
            errorDetails: str = traceback.format_exc()
            if logService is not None:
                logService.error(errorDetails)
            print('\nStack Trace:\n ' + str(errorDetails))
