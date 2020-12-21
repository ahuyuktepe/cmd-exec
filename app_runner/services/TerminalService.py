from app_runner.enums.UIColor import UIColor
from app_runner.services.BaseService import BaseService
from app_runner.services.LogService import LogService
from app_runner.ui_elements.TerminalScreen import TerminalScreen
from app_runner.utils.ErrorUtil import ErrorUtil
from app_runner.utils.ValidationUtil import ValidationUtil


class TerminalService(BaseService):
    __screen: TerminalScreen = None
    __logService: LogService = None

    def __init__(self, screen: TerminalScreen):
        self.__screen = screen

    def displayView(self, data):
        try:
            ValidationUtil.failIfObjNone(data, 'Given data object to view is null.')
            self.__screen.displayView(data)
        except Exception as exception:
            logService = self._appContext.getService('logService')
            ErrorUtil.handleException(exception, logService)
            self.__screen.clear()
            self.__screen.print(1, 1, 'Error:', UIColor.ERROR_MESSAGE_COLOR)
            self.__screen.print(3, 2, str(exception), UIColor.ERROR_MESSAGE_COLOR)
            self.__screen.print(1, 4, "Press 'q' to quit.", UIColor.WARNING_MESSAGE_COLOR)
            self.__screen.refresh()
