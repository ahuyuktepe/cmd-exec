from classes.app.MainAppConfig import MainAppConfig
from classes.menu.Menu import Menu
from classes.services.ArgumentService import ArgumentService
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
        self.__services['menuService'] = MenuService()
        self.__services['logService'].debug('AppContext: Instantiated all default services.')

    def getService(self, name: str) -> object:
        print('AppContext.getService(name:' + name + ')')
        return self.__services[name]

    def getMenu(self, menuId: str) -> Menu:
        print('AppContext.getMenu(menuId:' + menuId + ')')
        pass

    def addMenu(self, menu: Menu):
        print('AppContext.addMenu(menu)')
        pass
