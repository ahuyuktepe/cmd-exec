from src.builder.ModuleBuilder import ModuleBuilder
from src.context.AppContext import AppContext
from src.util.FileUtil import FileUtil
from src.util.ValidationUtil import ValidationUtil


class AppContextBuilder:

    @staticmethod
    def buildBaseAppContext() -> AppContext:
        appContext = AppContext()
        # Init Module Configs
        filePaths = FileUtil.getModuleConfigFilePaths()
        AppContextBuilder.__initConfigs(appContext, filePaths)

        # Init Module Settings
        filePaths = FileUtil.getModuleSettingFilePaths()
        AppContextBuilder.__initModules(appContext, filePaths)
        # Validate Modules
        AppContextBuilder.__validateModuleDependencies(appContext)
        # Init Services
        # serviceSettings = appContext.getSetting('core', 'services')
        # AppContextBuilder.__initServices(appContext, serviceSettings)
        return appContext

    # Private Methods

    # === Configs ===

    @staticmethod
    def __initConfigs(appContext: AppContext, filePaths: list):
        for filePath in filePaths:
            ValidationUtil.failIfFileIsNotReadable(filePath, 'ERRO5', {'path': filePath})
            configProps = FileUtil.generateObjFromYamlFile(filePath)
            AppContextBuilder.__validateConfigs(configProps, filePath)
            appContext.addConfig(configProps)

    # === Modules ===

    @staticmethod
    def __validateConfigs(configs: dict, configFilePath: str):
        for key, value in configs.items():
            ValidationUtil.failIfStringContainsChars(key, [':'], 'ERR18', {'key': key, 'path': configFilePath})
            if isinstance(value, dict):
                AppContextBuilder.__validateConfigs(value, configFilePath)

    @staticmethod
    def __initModules(appContext: AppContext, filePaths: list):
        for filePath in filePaths:
            module = ModuleBuilder.buildModule(filePath)
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

    # === Services ===

    @staticmethod
    def __initServices(appContext: AppContext, serviceProps: list):
        for props in serviceProps:
            appContext.addService(props)
