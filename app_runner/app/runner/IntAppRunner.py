from app_runner.app.context.AppContext import AppContext
from app_runner.app.runner.ApplicationRunner import ApplicationRunner
from app_runner.services.TerminalService import TerminalService
from app_runner.ui.element.UIView import UIView
import time


class IntAppRunner(ApplicationRunner):
    __terminalService: TerminalService

    def __init__(self, context: AppContext):
        super().__init__(context)
        self.__terminalService = context.getService('terminalService')

    def run(self):
        print('run')
        # View
        view: UIView = self.__terminalService.buildView('test')
        self.__terminalService.displayView(view)
        time.sleep(3)
