from src.context.AppContext import AppContext
from src.context.AppContextManager import AppContextManager
from src.module.AppModule import AppModule
from src.service.ArgumentService import ArgumentService
from src.service.ServiceType import ServiceType
from src.service.ServiceBuilder import ServiceBuilder
from src.util.ListUtil import ListUtil
from src.util.ModuleUtil import ModuleUtil


class AppContextBuilder:

    @staticmethod
    def buildBaseAppContext() -> AppContext:
        appContext = AppContext()
        names = ModuleUtil.getModuleNames()
        # Init Modules
        AppContextBuilder.__initModules(appContext, names)
        AppContextBuilder.__validateModuleDependencies(appContext)
        # Init Module Configs
        AppContextBuilder.__initConfigs(appContext, names)
        # Init Services
        AppContextBuilder.__initCoreServices(appContext)
        AppContextBuilder.__initCustomServices(appContext, names)
        return appContext

    # Private Methods

    # === Service ===

    @staticmethod
    def __initCoreServices(appContext: AppContext):
        # Initialize Core Services
        # ConfigurationService
        service = ServiceBuilder.buildConfigService(appContext)
        appContext.addService(ServiceType.CONF_SERVICE, service)
        # ArgumentService
        service = ServiceBuilder.buildArgService(appContext)
        appContext.addService(ServiceType.ARG_SERVICE, service)
        # FieldService
        service = ServiceBuilder.buildFieldService(appContext)
        appContext.addService(ServiceType.FIELD_SERVICE, service)
        # CommandService
        service = ServiceBuilder.buildCommandService(appContext)
        appContext.addService(ServiceType.CMD_SERVICE, service)
        # LogService
        service = ServiceBuilder.buildLogService(appContext)
        appContext.addService(ServiceType.LOG_SERVICE, service)
        # TerminalService
        service = ServiceBuilder.buildTerminalService(appContext)
        appContext.addService(ServiceType.TERMINAL_SERVICE, service)

    @staticmethod
    def __initCustomServices(appContext: AppContext, names: list):
        for name in names:
            module: AppModule = appContext.getModule(name)
            if module is not None:
                services: dict = module.findAllServicePropertiesByInit(True)
                for sid, serviceProps in services.items():
                    if not appContext.hasService(sid):
                        service = ServiceBuilder.buildService(serviceProps, appContext)
                        appContext.addService(sid, service)

    # === Configs ===

    @staticmethod
    def __initConfigs(appContext: AppContext, names: list):
        # Insert Main Config
        props: dict = ModuleUtil.getMainConfig()
        appContext.addConfig(props)
        # Insert Module Configs
        for name in names:
            if ModuleUtil.doesConfigFileExistForModule(name):
                props = ModuleUtil.getModuleConfigs(name)
                ModuleUtil.validateModuleConfigs(name, props)
                appContext.addConfig(props)

    # === Modules ===

    @staticmethod
    def __initModules(appContext: AppContext, names: list):
        for name in names:
            # Validate Files
            ModuleUtil.validateModuleDirectoryAndFiles(name)
            # Validate Properties
            props = ModuleUtil.getModuleSettings(name)
            ModuleUtil.validateModuleProperties(name, props)
            # Generate Module Object
            module = AppModule(props['name'], props['version'], props.get('description'))
            # Build dependencies
            dependencies = props.get('dependencies')
            if dependencies is not None:
                module.setDependencies(dependencies)
            # Insert Services
            services = props.get('services')
            if services is not None:
                module.setServiceProperties(services)
            appContext.addModule(module)

    @staticmethod
    def __validateModuleDependencies(appContext: AppContext):
        modules = appContext.getModules()
        for module in modules:
            for dependency in module.getDependencies():
                name = dependency.getModuleName()
                moduleExist = appContext.hasModule(name)
                trgVersion = None
                if moduleExist:
                    trgModule = appContext.getModule(name)
                    trgVersion = trgModule.getVersion()
                dependency.validate(module.getName(), trgVersion, moduleExist)
