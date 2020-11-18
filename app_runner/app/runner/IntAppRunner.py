from app_runner.app.context.AppContext import AppContext
from app_runner.app.runner.ApplicationRunner import ApplicationRunner
from app_runner.errors.UIError import UIError
from app_runner.menu.Command import Command
from app_runner.menu.Menu import Menu
from app_runner.services.CommandService import CommandService
from app_runner.services.MenuService import MenuService
from app_runner.services.UIService import UIService


class IntAppRunner(ApplicationRunner):
    __uiService: UIService
    __commandService: CommandService

    def __init__(self, context: AppContext):
        super().__init__(context)
        self.__uiService = context.getService('uiService')
        self.__commandService = context.getService('commandService')

    def run(self):
        try:
            # 1) Build Menu
            menuService: MenuService = self._appContext.getService('menuService')
            menu: Menu = menuService.buildMenu('main')
            # 2) Get Command
            # cmd: Command = self.__uiService.getSelectedCommand()
            cmd: Command = menu.getCommand('details')
            # 3) Collect command arguments from user
            # values: dict = self.__uiService.collectCmdArguments(cmd)
            values: dict = {
                'id': 1
            }
            # 4) Execute command
            self.__commandService.execute(cmd, values)
        except UIError as uiErr:
            print(uiErr)
