from app_runner.app.MainAppConfig import MainAppConfig
from app_runner.menu.Menu import Menu
from app_runner.utils.ObjUtil import ObjUtil
from app_runner.utils.StrUtil import StrUtil


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
        service: object = self.__services.get(name)
        if service is None:
            props = StrUtil.getServicePropertiesFromStr(name)
            service = self.__initializeService(
                props.get('module'),
                props.get('class')
            )
            service.setAppContext(self)
            self.addService(name, service)
        return service

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

    def __initializeService(self, mid: str, clsName: str):
        package: str
        if mid is None:
            package = 'services' + clsName
        else:
            package = 'modules.' + mid + '.src.services'
        cls = ObjUtil.getClassFromStr(package, clsName)
        return cls()
