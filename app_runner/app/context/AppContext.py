from app_runner.app.config.AppConfig import AppConfig
from app_runner.app.config.MainAppConfig import MainAppConfig
from app_runner.menu.Menu import Menu
from app_runner.utils.FileUtil import FileUtil
from app_runner.utils.ObjUtil import ObjUtil
from app_runner.utils.StrUtil import StrUtil
from app_runner.utils.ValidationUtil import ValidationUtil


class AppContext:
    __mainConfig: MainAppConfig
    __services: dict
    __executors: dict
    __validators: dict
    __valueGetters: dict
    __configs: dict
    __menus: dict

    def __init__(self):
        self.__services = {}
        self.__executors = {}
        self.__validators = {}
        self.__valueGetters = {}
        self.__configs = {}
        self.__menus = {}

    # Getter Methods

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

    def getConfig(self, name: str) -> object:
        config: AppConfig = self.__configs.get(name)
        if config is None:
            self.initializeConfig(name)
            config = self.__configs.get(name)
        return config

    # Setter Methods

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

    # Flow Methods

    def initializeConfig(self, name: str):
        if name is not None:
            props = StrUtil.getFilePropertiesFromStr(name)
            config = self.__initializeConfig(
                props.get('module'),
                props.get('file')
            )
            self.addConfig(name, config)

    # Private Methods

    def __initializeService(self, mid: str, clsName: str):
        package: str
        if mid is None:
            package = 'services.' + clsName
        else:
            package = 'modules.' + mid + '.src.services'
        FileUtil.failIfClassFileNotDefined(mid, clsName, 'services')
        cls = ObjUtil.getClassFromStr(package, clsName)
        return cls()

    def __initializeConfig(self, mid: str, fileName: str):
        filePath = FileUtil.getAbsolutePath(['modules', mid, 'conf', fileName]) + '.yaml'
        props = FileUtil.generateObjFromYamlFile(filePath)
        ValidationUtil.failIfObjNone(props, "No properties available in configuration file '" + filePath + "'.")
        return AppConfig(props)
