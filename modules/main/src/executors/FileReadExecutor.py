from app_runner.extension.ContextAware import ContextAware
from app_runner.services.UIService import UIService
import time


class FileReadExecutor(ContextAware):

    def readFile(self, values: dict):
        uiService: UIService = self._appContext.getService('uiService')
        uiService.displayView('text', {})
        # EventManager.triggerEvent(FlowEventType.APPEND_TEXT, {
        #     'text': 'This is a test message.'
        # })
        time.sleep(3)
