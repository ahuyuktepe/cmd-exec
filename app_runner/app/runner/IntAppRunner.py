from app_runner.app.context.AppContext import AppContext
from app_runner.app.runner.ApplicationRunner import ApplicationRunner
from app_runner.services.CommandService import CommandService
from app_runner.services.TerminalService import TerminalService

class IntAppRunner(ApplicationRunner):
    __terminalService: TerminalService
    __commandService: CommandService
    __quit: bool

    def __init__(self, context: AppContext):
        super().__init__(context)
        self.__quit = False
        self.__terminalService = context.getService('terminalService')
        self.__commandService = context.getService('commandService')

    def run(self):
        self.__terminalService.displayView({'vid': 'core.test'})
