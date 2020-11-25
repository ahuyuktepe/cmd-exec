from app_runner.app.context.AppContext import AppContext
from app_runner.app.runner.ApplicationRunner import ApplicationRunner
from app_runner.errors.UIError import UIError
from app_runner.menu.Command import Command
from app_runner.services.CommandService import CommandService
from app_runner.services.UIService import UIService
import time

class IntAppRunner(ApplicationRunner):
    __uiService: UIService
    __commandService: CommandService

    def __init__(self, context: AppContext):
        super().__init__(context)
        self.__uiService = context.getService('uiService')
        self.__commandService = context.getService('commandService')

    # def run(self):
    #     self.__uiService.displayView('test')
    #     time.sleep(1)

    def run(self):
        try:
            # 1) Get Command
            cmd: Command = self.__uiService.getSelectedCommand()
            while cmd is not None and cmd.getId() != 'exit':
                # 2) Collect command arguments from user
                values: dict = self.__uiService.collectCmdArguments(cmd)
                # 3) Execute command
                self.__commandService.execute(cmd, values)
                # 4) Get Command
                cmd: Command = self.__uiService.getSelectedCommand()
            print('Bye Bye')
        except UIError as uiErr:
            print(uiErr)
