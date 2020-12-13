from app_runner.app.context.AppContext import AppContext
from app_runner.app.runner.ApplicationRunner import ApplicationRunner
from app_runner.errors.UIError import UIError
from app_runner.menu.Command import Command
from app_runner.menu.Menu import Menu
from app_runner.services.CommandService import CommandService
from app_runner.services.MenuService import MenuService
from app_runner.services.UIService import UIService
from app_runner.utils.FileUtil import FileUtil
import time


class IntAppRunner(ApplicationRunner):
    __uiService: UIService
    __commandService: CommandService

    def __init__(self, context: AppContext):
        super().__init__(context)
        self.__uiService = context.getService('uiService')
        self.__commandService = context.getService('commandService')

    def run(self):
        self.runWithTextView()
        # self.runWithMenu()
        # self.runWithFormView()
        # self.runWithXmlView()

    def runWithTextView(self):
        self.__uiService.displayView('text', {})
        time.sleep(3)

    def runWithXmlView(self):
        htmlText = FileUtil.readFile('temp/sample.xml')
        self.__uiService.displayXml(htmlText)

    def runWithFormView(self):
        menuService: MenuService = self._appContext.getService('menuService')
        menu: Menu = menuService.buildMenu('main')
        cmd: Command = menu.getCommand('displayXml')
        values: dict = self.__uiService.collectCmdArguments(cmd)
        print('Values: ' + str(values))

    def runWithMenu(self):
        try:
            # 1) Get Command
            cmd: Command = self.__uiService.getSelectedCommand()
            while cmd is not None and cmd.getId() != 'exit':
                # 2) Collect command arguments from user
                values: dict = {}
                if cmd.hasFields():
                    values: dict = self.__uiService.collectCmdArguments(cmd)
                # 3) Execute command
                self.__commandService.execute(cmd, values)
                # 4) Get Command
                cmd: Command = self.__uiService.getSelectedCommand()
            print('Bye Bye')
        except UIError as uiErr:
            print(uiErr)

