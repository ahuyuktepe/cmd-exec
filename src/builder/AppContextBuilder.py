from src.context.AppContext import AppContext
<<<<<<< HEAD
=======
from src.module.AppModule import AppModule
from src.util.ModuleUtil import ModuleUtil
>>>>>>> refactoring


class AppContextBuilder:

    @staticmethod
    def buildBaseAppContext() -> AppContext:
        appContext = AppContext()
<<<<<<< HEAD
        appContext.initializeConfig('main')
        return appContext
=======
        # Init Modules
        AppContextBuilder.__initModules(appContext)
        AppContextBuilder.__validateModuleDependencies(appContext)
        # Init Module Configs
        # filePaths = ModuleUtil.getConfigFilePaths()
        # AppContextBuilder.__initConfigs(appContext, filePaths)
        # Init Services
        # serviceSettings = appContext.getSetting('core', 'services')
        # AppContextBuilder.__initServices(appContext, serviceSettings)
        return appContext

    # Private Methods

    # === Modules ===

    @staticmethod
    def __initModules(appContext: AppContext):
        names = ModuleUtil.getModuleNames()
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
                for dependency in dependencies:
                    module.addDependency(dependency)
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

    # === Configs ===

    # @staticmethod
    # def __initConfigs(appContext: AppContext, filePaths: list):
    #     for filePath in filePaths:
    #         ValidationUtil.failIfFileIsNotReadable(filePath, 'ERRO5', {'path': filePath})
    #         configProps = FileUtil.generateObjFromYamlFile(filePath)
    #         AppContextBuilder.__validateConfigs(configProps, filePath)
    #         appContext.addConfig(configProps)

    # @staticmethod
    # def __validateConfigs(configs: dict, configFilePath: str):
    #     for key, value in configs.items():
    #         ValidationUtil.failIfStringContainsChars(key, [':'], 'ERR18', {'key': key, 'path': configFilePath})
    #         if isinstance(value, dict):
    #             AppContextBuilder.__validateConfigs(value, configFilePath)

    # === Services ===

    # @staticmethod
    # def __initServices(appContext: AppContext, serviceProps: list):
    #     for props in serviceProps:
    #         appContext.addService(props)
>>>>>>> refactoring
