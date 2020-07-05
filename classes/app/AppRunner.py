from classes.app.AppContext import AppContext
from classes.app.MainAppConfig import MainAppConfig
from classes.menu.Menu import Menu
from classes.services.ArgumentService import ArgumentService
from classes.services.LogService import LogService
from classes.services.MenuService import MenuService
from classes.utils.FileUtil import FileUtil

class AppRunner:
    __argumentService: ArgumentService
    __appContext: AppContext
    __logService: LogService
    __menuService: MenuService

    def __init__(self, configPath: str):
        mainAppConfig = MainAppConfig(configPath)
        self.__appContext = AppContext(mainAppConfig)
        self.__argumentService = self.__appContext.getService('argumentService')
        self.__logService = self.__appContext.getService('logService')
        self.__menuService = self.__appContext.getService('menuService')

    def run(self):
        self.__logService.debug('AppRunner: Passed arguments : ' + self.__argumentService.getPassedArgumentsAsStr())
        if self.__argumentService.isCmdMode():
            self.__runInCmdMode()
        elif self.__argumentService.isInteractiveMode():
            self.__runInInteractiveMode()

    def __runInCmdMode(self):
        print('Running in command mode')
        menuId = self.__argumentService.getMenu()
        obj = FileUtil.generateObjFromJsonFile('menus/{menu}-menu.json'.format(menu=menuId))
        menu: Menu = self.__menuService.buildMenu(obj)

    def __runInInteractiveMode(self):
        pass
