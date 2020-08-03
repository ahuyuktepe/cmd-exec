
class FieldValidationError:
    __msg: str

    def __init__(self, msg: str):
        self.__msg = msg

    def getMsg(self) -> str:
        return self.__msg
