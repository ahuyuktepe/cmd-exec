from app_runner.errors.FieldValidationError import FieldValidationError


class FieldValidationErrors:
    __errors: list

    def __init__(self):
        self.__errors = []

    # Getter Methods

    def getErrorCount(self) -> int:
        return len(self.__errors)

    def getErrorByFid(self, fid: str) -> FieldValidationError:
        for error in self.__errors:
            if error.getFid() == fid:
                return error
        return None

    def getErrors(self) -> list:
        return self.__errors

    def hasErrors(self) -> bool:
        return len(self.__errors) > 0

    def getErrorByIndex(self, index: int) -> FieldValidationError:
        return self.__errors[index]

    # Setter Methods

    def addError(self, error: FieldValidationError):
        self.__errors.append(error)

    def addErrors(self, errors: list):
        for error in errors:
            self.addError(error)

    def clearErrors(self):
        self.__errors.clear()

    # Other Methods

    def printErrors(self):
        error: FieldValidationError
        retStr: str = '\nField Validation Errors \n'
        for error in self.__errors:
            retStr += "\n - " + error.getMsg()
        print(retStr)
