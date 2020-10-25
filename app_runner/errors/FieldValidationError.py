
class FieldValidationError:
    __fid: str
    __msg: str

    def __init__(self, msg: str, fid: str):
        self.__msg = msg
        self.__fid = fid

    # Getter Methods

    def getFid(self) -> str:
        return self.__fid

    def getMsg(self) -> str:
        return self.__msg
