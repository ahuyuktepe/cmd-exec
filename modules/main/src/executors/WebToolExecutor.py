from app_runner.extension.ContextAware import ContextAware
from app_runner.services.UIService import UIService


class WebToolExecutor(ContextAware):

    def getName(self, values: dict):
        uiService: UIService = self._appContext.getService('uiService')
        uiService.displayText('Response: ' + str(values))
