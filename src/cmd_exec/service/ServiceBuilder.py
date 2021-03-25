from cmd_exec.context.AppContextManager import AppContextManager
from cmd_exec.error.CmdExecError import CmdExecError
from cmd_exec.module.ServiceProperties import ServiceProperties
from cmd_exec.service.AppService import AppService
from cmd_exec.service.ArgumentService import ArgumentService
from cmd_exec.service.CommandService import CommandService
from cmd_exec.service.ConfigurationService import ConfigurationService
from cmd_exec.service.ServiceType import ServiceType
from cmd_exec.service.FieldService import FieldService
from cmd_exec.service.LogService import LogService
from cmd_exec.service.TerminalService import TerminalService
from cmd_exec.util.ObjUtil import ObjUtil
from cmd_exec.util.StrUtil import StrUtil
from cmd_exec.util.ValidationUtil import ValidationUtil


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
        confService = appContext.getService(ServiceType.CONF_SERVICE)
        service = ArgumentService(confService)
        service.setContextManager(context)
        return service

    @staticmethod
    def buildCommandService(appContext) -> CommandService:
        context = AppContextManager(appContext)
        fieldService = appContext.getService(ServiceType.FIELD_SERVICE)
        argService = appContext.getService(ServiceType.ARG_SERVICE)
        service = CommandService(fieldService, argService)
        service.setContextManager(context)
        return service

    @staticmethod
    def buildFieldService(appContext) -> FieldService:
        context = AppContextManager(appContext)
        configService = appContext.getService(ServiceType.CONF_SERVICE)
        argService = appContext.getService(ServiceType.ARG_SERVICE)
        service = FieldService(configService, argService)
        service.setContextManager(context)
        return service

    @staticmethod
    def buildLogService(appContext) -> LogService:
        context = AppContextManager(appContext)
        confService = appContext.getService(ServiceType.CONF_SERVICE)
        service = LogService(confService)
        service.setContextManager(context)
        return service

    @staticmethod
    def buildTerminalService(appContext) -> LogService:
        context = AppContextManager(appContext)
        service = TerminalService()
        service.setContextManager(context)
        return service
