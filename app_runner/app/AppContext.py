from app_runner.app.MainAppConfig import MainAppConfig
from app_runner.menu.Menu import Menu

class AppContext:
    __mainConfig: MainAppConfig
    __services: dict = {}
    __executors: dict = {}
    __validators: dict = {}
    __valueGetters: dict = {}
    __configs: dict = {}
    __menus: dict = {}

    def __init__(self, mainConfig: MainAppConfig):
        self.__mainConfig = mainConfig
        self.addConfig('main', mainConfig)

    def addService(self, name: str, service: object):
        self.__services[name] = service

    def addExecutor(self, name: str, executor: object):
        self.__executors[name] = executor

    def addValidator(self, name: str, validator: object):
        self.__validators[name] = validator

    def addValueGetter(self, name: str, valueGetter: object):
        self.__valueGetters[name] = valueGetter

    def addMenu(self, name: str, menu: Menu):
        self.__menus[name] = menu

    def addConfig(self, name: str, config: object):
        self.__configs[name] = config

    def getService(self, name: str) -> object:
        return self.__services.get(name)

    def getExecutor(self, name: str) -> object:
        return self.__executors.get(name)

    def getValidator(self, name: str) -> object:
        return self.__validators.get(name)

    def getValueGetter(self, name: str) -> object:
        return self.__valueGetters.get(name)

    def getMenu(self, name: str) -> Menu:
        return self.__menus.get(name)

    def getConfig(self, name: str) -> object:
        return self.__configs.get(name)
