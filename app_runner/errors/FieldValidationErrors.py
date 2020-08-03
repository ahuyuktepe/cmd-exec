from app_runner.errors.FieldValidationError import FieldValidationError


class FieldValidationErrors:
    __errors: list = []

    def addError(self, error: FieldValidationError):
        self.__errors.append(error)

    def hasErrors(self) -> bool:
        return len(self.__errors) > 0

    def getErrors(self) -> list:
        return self.__errors

    def printErrors(self):
        error: FieldValidationError
        retStr: str = 'Field Validation Errors \n'
        for error in self.__errors:
            retStr += ' - ' + error.getMsg() + '\n'
        print(retStr)
