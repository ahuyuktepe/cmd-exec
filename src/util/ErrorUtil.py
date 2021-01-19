import traceback


class ErrorUtil:
    @staticmethod
    def handleException(exception: Exception):
        print('Error occurred while running application.')
        print('\nError Details:\n' + str(exception))
        errorDetails: str = traceback.format_exc()
        print('\nStack Trace:\n ' + str(errorDetails))
