from src.context.AppContextManager import AppContextManager
from src.error.CmdExecError import CmdExecError
from src.module.ServiceProperties import ServiceProperties
from src.service.AppService import AppService
from src.service.ArgumentService import ArgumentService
from src.service.CommandService import CommandService
from src.service.ConfigurationService import ConfigurationService
from src.service.CoreServiceType import CoreServiceType
from src.service.FieldService import FieldService
from src.service.LogService import LogService
from src.util.ObjUtil import ObjUtil
from src.util.StrUtil import StrUtil
from src.util.ValidationUtil import ValidationUtil


class ServiceBuilder:

    @staticmethod
    def buildService(serviceProps: ServiceProperties, appContext):
        if serviceProps is None:
            raise CmdExecError('ERR27')
        # Init service and return
        args = serviceProps.getArgs()
        passedArgs = []
        for arg in args:
            if arg['type'] == 'service':
                sid = arg['value']
                if appContext.hasService(sid):
                    service = appContext.getService(sid)
                else:
                    props = ServiceBuilder.getServiceProperties(sid, appContext)
                    service = ServiceBuilder.buildService(props, appContext)
                    appContext.addService(sid, service)
                passedArgs.append(service)
            elif arg['type'] == 'configs':
                configs = appContext.getConfigs()
                passedArgs.append(configs)
            else:
                passedArgs.append(arg['value'])
        clsPath = serviceProps.getClassPath()
        clsName = serviceProps.getClassName()
        ValidationUtil.failIfClassFileDoesNotExist(clsPath, 'ERR30', {'cls': clsName, 'path': clsPath})
        cls = ObjUtil.getClassFromClsPath(clsPath, clsName)
        if not issubclass(cls, AppService):
            raise CmdExecError('ERR28', {'src': clsName})
        service = ObjUtil.initClassFromStr(clsPath, clsName, passedArgs)
        contextManager = AppContextManager(appContext)
        service.setContextManager(contextManager)
        return service

    @staticmethod
    def getServiceProperties(sid, appContext) -> ServiceProperties:
        values = StrUtil.getModuleServiceMapFromStr(sid)
        mid = values.get('mid')
        if mid is not None:
            sid = values.get('sid')
            module = appContext.getModule(mid)
            return module.getServicePropertiesById(sid)
        else:
            for module in appContext.getModules():
                props = module.getServicePropertiesById(sid)
                if props is not None:
                    return props
        return None

    @staticmethod
    def buildConfigService(appContext) -> ConfigurationService:
        context = AppContextManager(appContext)
        configs = appContext.getConfigs()
        service = ConfigurationService(configs)
        service.setContextManager(context)
        return service

    @staticmethod
    def buildArgService(appContext) -> ArgumentService:
        context = AppContextManager(appContext)
        confService = appContext.getService(CoreServiceType.CONF_SERVICE)
        service = ArgumentService(confService)
        service.setContextManager(context)
        return service

    @staticmethod
    def buildCommandService(appContext) -> CommandService:
        context = AppContextManager(appContext)
        fieldService = appContext.getService(CoreServiceType.FIELD_SERVICE)
        argService = appContext.getService(CoreServiceType.ARG_SERVICE)
        service = CommandService(fieldService, argService)
        service.setContextManager(context)
        return service

    @staticmethod
    def buildFieldService(appContext) -> FieldService:
        context = AppContextManager(appContext)
        configService = appContext.getService(CoreServiceType.CONF_SERVICE)
        argService = appContext.getService(CoreServiceType.ARG_SERVICE)
        service = FieldService(configService, argService)
        service.setContextManager(context)
        return service

    @staticmethod
    def buildLogService(appContext) -> LogService:
        context = AppContextManager(appContext)
        confService = appContext.getService(CoreServiceType.CONF_SERVICE)
        service = LogService(confService)
        service.setContextManager(context)
        return service
