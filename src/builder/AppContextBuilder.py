from src.context.AppContext import AppContext
from src.context.AppContextManager import AppContextManager
from src.module.AppModule import AppModule
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
        ListUtil.deleteStr(names, 'core')
        # Init Module Configs
        AppContextBuilder.__initConfigs(appContext, names)
        # Init Services
        AppContextBuilder.__initServices(appContext, names)
        return appContext

    # Private Methods

    # === Service ===

    @staticmethod
    def __initServices(appContext: AppContext, names: list):
        AppContextBuilder.__addService(appContext, 'core')
        for name in names:
            AppContextBuilder.__addService(appContext, name)

    @staticmethod
    def __addService(appContext: AppContext, name: str):
        module: AppModule = appContext.getModule(name)
        if module is not None:
            services: dict = module.findAllServicePropertiesByInit(True)
            for sid, modService in services.items():
                if not appContext.hasService(sid):
                    service = appContext.initService(modService)
                    context = AppContextManager(appContext)
                    service.setContextManager(context)
                    appContext.addService(sid, service)

    # === Configs ===

    @staticmethod
    def __initConfigs(appContext: AppContext, names: list):
        AppContextBuilder.__addConfigToAppContext('core', appContext)
        for name in names:
            AppContextBuilder.__addConfigToAppContext(name, appContext)

    @staticmethod
    def __addConfigToAppContext(name: str, appContext: AppContext):
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
