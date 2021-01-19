<<<<<<< HEAD
from src.config.AppConfig import AppConfig
from src.utils.FileUtil import FileUtil
from src.utils.StrUtil import StrUtil
from src.utils.ValidationUtil import ValidationUtil


class AppContext:
    __configs: dict

    def __init__(self):
        self.__configs = {}

    # Utility Methods

    def initializeConfig(self, name: str):
        if name is not None:
            props = StrUtil.getFilePropertiesFromStr(name)
            # Parse Config Name
            mid = props.get('module')
            fileName = props.get('file')
            filePath = FileUtil.getAbsolutePath(['modules', mid, 'conf', fileName]) + '.yaml'
            configProps = FileUtil.generateObjFromYamlFile(filePath)
            ValidationUtil.failIfObjNone(props, "No properties available in configuration file '" + filePath + "'.")
            # Add Configuration
            self.__configs[name] = AppConfig(configProps)
=======
from src.config.AppConfigs import AppConfigs
from src.module.AppModule import AppModule
from src.util.ObjUtil import ObjUtil


class AppContext:
    __configs: AppConfigs
    __services: dict
    __modules: dict

    def __init__(self):
        self.__configs = AppConfigs()
        self.__services = {}
        self.__modules = {}

    # Getter Methods

    def getConfig(self, key: str) -> object:
        return self.__configs.getValue(key)

    def getService(self, sid: str):
        return self.__services[sid]

    def getModules(self) -> list:
        return list(self.__modules.values())

    def getModule(self, name: str) -> AppModule:
        return self.__modules[name]

    def hasModule(self, name: str):
        module = self.__modules.get(name)
        return module is not None

    # Setter Methods

    def addModule(self, module: AppModule):
        name = module.getName()
        self.__modules[name] = module

    def addConfig(self, configs: dict):
        if configs is not None:
            self.__configs.addConfig(configs)

    def addService(self, props: dict):
        args = self.__buildArguments(props.get('args'))
        service = ObjUtil.initClassFromStr(props['path'], props['class'], args)
        service.setAppContext(self)
        sid = props['id']
        self.__services[sid] = service

    # Private Metdhods

    def __buildArguments(self, args: list) -> list:
        if args is None:
            return None
        retArgs = []
        for arg in args:
            if arg == 'appConfigs':
                retArgs.append(self.__configs)
            else:
                retArgs.append(arg)
        return retArgs

    def printConfigs(self):
        self.__configs.print()
>>>>>>> refactoring