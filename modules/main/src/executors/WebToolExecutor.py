from app_runner.extension.ContextAware import ContextAware
from app_runner.services.TerminalService import TerminalService
from app_runner.utils.FileUtil import FileUtil

class WebToolExecutor(ContextAware):

    def printText(self, values: dict):
        terminalService: TerminalService = self._appContext.getService('terminalService')
        terminalService.displayView({'vid': 'test'})

    def printHtml(self, values: dict):
        terminalService: TerminalService = self._appContext.getService('terminalService')
        htmlText = FileUtil.readFile('temp/sample.xml')
        terminalService.displayHtml(htmlText)
        terminalService.displayMessage('This is a test html page.')
