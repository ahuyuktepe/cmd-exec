from src.config.AppConfigs import AppConfigs
from src.error.CmdExecError import CmdExecError
from src.module.AppModule import AppModule
from src.module.ServiceProperties import ServiceProperties
from src.util.ObjUtil import ObjUtil
from src.util.StrUtil import StrUtil
from src.util.ValidationUtil import ValidationUtil


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
        if not self.hasService(sid):
            serviceProperties = self.getServiceProperties(sid)
            service = self.initService(serviceProperties)
            self.addService(sid, service)
        return self.__services.get(sid)

    def getModules(self) -> list:
        return list(self.__modules.values())

    def getModule(self, name: str) -> AppModule:
        return self.__modules.get(name)

    def getServiceProperties(self, sid: str) -> ServiceProperties:
        values = StrUtil.getModuleServiceMapFromStr(sid)
        mid = values.get('mid')
        if mid is not None:
            sid = values.get('sid')
            module = self.getModule(mid)
            return module.getServicePropertiesById(sid)
        else:
            for mid, module in self.__modules.items():
                props = module.getServicePropertiesById(sid)
                if props is not None:
                    return props
        return None

    def hasModule(self, name: str):
        module = self.__modules.get(name)
        return module is not None

    def hasService(self, sid: str):
        service = self.__services.get(sid)
        return service is not None

    def getInstancesByStr(self, ids: list) -> list:
        retList = []
        if ids is not None:
            for id in ids:
                if id == 'appConfigs':
                    retList.append(self.__configs)
                elif id.startswith('@'):
                    sid = id[1:]
                    service = self.getService(sid)
                    retList.append(service)
                else:
                    retList.append(id)
        return retList

    # Setter Methods

    def addModule(self, module: AppModule):
        name = module.getName()
        self.__modules[name] = module

    def addConfig(self, configs: dict):
        if configs is not None:
            self.__configs.addConfig(configs)

    def addService(self, sid: str, service: object):
        # Import class locally
        from src.service.AppService import AppService
        from src.context.AppContextManager import AppContextManager
        if service is None:
            raise CmdExecError('ERR26', {'sid': sid})
        elif not isinstance(service, AppService):
            raise CmdExecError('ERR28', {'cls': service.__class__.__name__})
        self.__services[sid] = service

    def printConfigs(self):
        self.__configs.print()

    # Utility Methods

    def initService(self, serviceProps: ServiceProperties) -> object:
        from src.service.AppService import AppService
        if serviceProps is None:
            raise CmdExecError('ERR27')
        # Init service and return
        args = serviceProps.getArgs()
        passedArgs = []
        for arg in args:
            if arg['type'] == 'service':
                sid = arg['value']
                if self.hasService(sid):
                    service = self.getService(sid)
                    self.addService(sid, service)
                else:
                    props = self.getServiceProperties(sid)
                    service = self.initService(props)
                    self.addService(sid, service)
                passedArgs.append(service)
            elif arg['type'] == 'configs':
                passedArgs.append(self.__configs)
            else:
                passedArgs.append(arg['value'])
        clsPath = serviceProps.getClassPath()
        clsName = serviceProps.getClassName()
        ValidationUtil.failIfClassFileDoesNotExist(clsPath, 'ERR30', {'cls': clsName, 'path': clsPath})
        cls = StrUtil.convertClassNameStrToClass(clsPath, clsName)
        if not issubclass(cls, AppService):
            raise CmdExecError('ERR33', {'src': clsName, 'parent': 'AppService', 'name': serviceProps.getModuleName()})
        return ObjUtil.initClassFromStr(clsPath, clsName, passedArgs)
