from classes.app.MainAppConfig import MainAppConfig
from classes.menu.Menu import Menu
from classes.services.ArgumentService import ArgumentService
from classes.services.CommandService import CommandService
from classes.services.FieldService import FieldService
from classes.services.LogService import LogService
from classes.services.MenuService import MenuService

class AppContext:
    __mainConfig: MainAppConfig
    __services: dict
    __executors: dict
    __validators: dict
    __valueGetters: dict
    __menus: dict

    def __init__(self, mainConfig: MainAppConfig):
        self.__mainConfig = mainConfig
        self.__services = {}
        self.__executors = {}
        self.__validators = {}
        self.__valueGetters = {}
        self.__menus = {}
        self.__initDefaultServices()

    def __initDefaultServices(self):
        self.__services['argumentService'] = ArgumentService()
        obj: dict = self.__mainConfig.getObjValue('log_settings')
        self.__services['logService'] = LogService(obj)
        self.__services['fieldService'] = FieldService()
        self.__injectCommandService()
        self.__injectMenuService()
        self.__services['logService'].debug('AppContext: Instantiated all default services.')

    def __injectCommandService(self):
        cmdService: CommandService = CommandService()
        cmdService.setLogService(self.getService('logService'))
        cmdService.setFieldService(self.getService('fieldService'))
        self.__services['commandService'] = cmdService

    def __injectMenuService(self):
        menuService: MenuService = MenuService()
        menuService.setCmdService(self.getService('commandService'))
        self.__services['menuService'] = menuService

    def getService(self, name: str) -> object:
        return self.__services[name]

    def getMenu(self, menuId: str) -> Menu:
        pass

    def addMenu(self, menu: Menu):
        pass
