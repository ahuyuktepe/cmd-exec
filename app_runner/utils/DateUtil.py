from datetime import date, datetime

class DateUtil:
    @staticmethod
    def getCurrentDateTimeAsStr(formatStr: str = "%Y-%m-%d %H:%M:%S") -> str:
        now = datetime.now()
        return now.strftime(formatStr)
