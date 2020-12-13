from app_runner.extension.ContextAware import ContextAware
from app_runner.services.TerminalService import TerminalService
from app_runner.services.UIService import UIService
from app_runner.utils.FileUtil import FileUtil
import time

class WebToolExecutor(ContextAware):

    def displayContent(self, values: dict):
        fileName = values.get('fileName')
        if fileName is None:
            fileName = 'sample'
        htmlText = FileUtil.readFile('temp/' + fileName + '.xml')
        terminalService: TerminalService = self._appContext.getService('terminalService')
        terminalService.displayView({'vid':'test'})

    def printText(self, values: dict):
        print('WebToolExecutor')
