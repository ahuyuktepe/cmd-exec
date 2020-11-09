from app_runner.app.context.AppContext import AppContext
from app_runner.app.runner.ApplicationRunner import ApplicationRunner
from app_runner.menu.Command import Command
from app_runner.menu.Menu import Menu
from app_runner.services.CommandService import CommandService
from app_runner.services.MenuService import MenuService
from app_runner.services.UIService import TerminalService


class IntAppRunner(ApplicationRunner):
    __terminalService: TerminalService
    __commandService: CommandService

    def __init__(self, context: AppContext):
        super().__init__(context)
        self.__terminalService = context.getService('terminalService')

    def run(self):
        # 1) Build Menu
        menuService: MenuService = self._appContext.getService('menuService')
        menu: Menu = menuService.buildMenu('main')
        print('1) Menu: ' + menu.getName())
        # 2) Get Command
        # cmd: Command = self.__terminalService.getSelectedCommand()
        cmd: Command = menu.getCommand('details')
        print('2) Command: ' + cmd.getDescription())
        # 3) Collect command arguments from user
        values: dict = self.__terminalService.collectCmdArguments(cmd)
        print('3) Values: '  + str(values))
        # 4) Execute command
        # self.__commandService.execute()
