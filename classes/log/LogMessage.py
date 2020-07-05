from classes.log.LogSettings import LogSettings
from classes.utils.DateUtil import DateUtil

class LogMessage:
    __level: str
    __message: str

    def __init__(self, level: str, msg: str):
        self.__level = level
        self.__message = msg

    def isLevel(self, level: str) -> bool:
        return self.__level == level

    def getFormattedMessage(self, settings: LogSettings) -> str:
        frmStr = settings.getMsgFormat()
        formattedMsg = frmStr.replace('{level}', '{:<8}'.format(self.__level.upper()))
        dateTimeStr = DateUtil.getCurrentDateTimeAsStr(settings.getDateFormat())
        formattedMsg = formattedMsg.replace('{date}', '{:<19}'.format(dateTimeStr))
        formattedMsg = formattedMsg.replace('{msg}', self.__message)
        return formattedMsg + '\n'
