from app_runner.app.AppConfig import AppConfig
from app_runner.app.MainAppConfig import MainAppConfig
from app_runner.menu.Menu import Menu
from app_runner.utils.FileUtil import FileUtil
from app_runner.utils.ObjUtil import ObjUtil
from app_runner.utils.StrUtil import StrUtil
from app_runner.utils.ValidationUtil import ValidationUtil


class AppContext:
    __mainConfig: MainAppConfig
    __services: dict = {}
    __executors: dict = {}
    __validators: dict = {}
    __valueGetters: dict = {}
    __configs: dict = {}
    __menus: dict = {}

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
        config: AppConfig = self.__configs.get(name)
        if config is None:
            props = StrUtil.getConfigPropertiesFromStr(name)
            config = self.__initializeConfig(
                props.get('module'),
                props.get('file')
            )
            self.addConfig(name, config)
        return config

    def __initializeService(self, mid: str, clsName: str):
        package: str
        if mid is None:
            package = 'services.' + clsName
        else:
            package = 'modules.' + mid + '.src.services'
        ValidationUtil.failIfServiceClassIsNotDefined(mid, clsName)
        cls = ObjUtil.getClassFromStr(package, clsName)
        return cls()

    def __initializeConfig(self, mid: str, fileName: str):
        filePath: str
        fileName = fileName + '.yaml'
        if mid is None:
            filePath = FileUtil.getAbsolutePath(['resources', 'conf', fileName])
        else:
            filePath = FileUtil.getAbsolutePath(['modules', mid, 'conf', fileName])
        ValidationUtil.failIfFileNotReadable(filePath)
        props = FileUtil.generateObjFromYamlFile(filePath)
        ValidationUtil.failIfObjNone(props, "No properties available in configuration file '" + filePath + "'.")
        return AppConfig(props)
