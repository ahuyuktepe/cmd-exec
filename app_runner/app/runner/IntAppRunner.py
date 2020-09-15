from app_runner.app.config.AppConfig import AppConfig
from app_runner.app.context.AppContext import AppContext
from app_runner.app.runner.ApplicationRunner import ApplicationRunner
from app_runner.menu.Menu import Menu
from app_runner.ui.terminal.MainScreen import MainScreen


class IntAppRunner(ApplicationRunner):

    def __init__(self, context: AppContext):
        super().__init__(context)

    def run(self):
        # 1) Print Screen
        screen: MainScreen = self.__buildScreen()
        # 2) Build & Add Menu
        menu: Menu = self._menuService.buildMenu('main')
        screen.addAndActivateMenu(menu)
        # 3) Print Screen
        screen.print()
        # 4) Get User Input
        userInput: str = None
        while userInput != 'q':
            userInput = screen.getUserInput()
            menu = self._menuService.buildMenu(userInput)
            if menu is not None:
                screen.addAndActivateMenu(menu)
                screen.refreshSection('body')

    def __buildScreen(self) -> MainScreen:
        config: AppConfig = self._appContext.getConfig('main')
        appName: str = config.getObjValue('application.name')
        screen: MainScreen = MainScreen(appName)
        screen.initialize()
        screen.buildSections()
        return screen
