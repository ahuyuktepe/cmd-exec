from app_runner.app.config.AppConfig import AppConfig
from app_runner.app.context.AppContext import AppContext
from app_runner.builders.BuilderFactory import BuilderFactory
from app_runner.builders.BuilderFactoryProducer import BuilderFactoryProducer
from app_runner.classes.KeyboardListener import KeyboardListener
from app_runner.classes.ViewManager import ViewManager
from app_runner.services.ArgumentService import ArgumentService
from app_runner.services.CommandService import CommandService
from app_runner.services.FieldService import FieldService
from app_runner.services.LogService import LogService
from app_runner.services.MenuService import MenuService
from app_runner.services.TerminalService import TerminalService
from app_runner.ui_elements.TerminalScreen import TerminalScreen


class AppContextBuilder:

    @staticmethod
    def updateContextForInteractiveMode(appContext: AppContext):
        # Instantiate Screen Dependencies
        builderFactory: BuilderFactory = BuilderFactoryProducer.getFactory('curses')
        viewBuilder = builderFactory.getViewBuilder()
        printAreaBuilder = builderFactory.getPrintAreaBuilder()
        # Initialize Screen
        screen = TerminalScreen(appContext, viewBuilder, printAreaBuilder)
        screen.setup()
        AppContextBuilder.__setTerminalService(screen, appContext)

    @staticmethod
    def updateContextForCommandMode(appContext: AppContext):
        pass

    @staticmethod
    def buildBaseAppContext() -> AppContext:
        appContext = AppContext()
        appContext.initializeConfig('core.main')
        AppContextBuilder.__setArgumentService(appContext)
        AppContextBuilder.__setLogService(appContext)
        AppContextBuilder.__setFieldService(appContext)
        AppContextBuilder.__setCommandService(appContext)
        AppContextBuilder.__setMenuService(appContext)
        return appContext

    @staticmethod
    def __setArgumentService(appContext: AppContext):
        appContext.addService('argumentService', ArgumentService())

    @staticmethod
    def __setLogService(appContext: AppContext):
        config: AppConfig = appContext.getConfig('core.main')
        obj: dict = config.getObjValue('log_settings')
        appContext.addService('logService', LogService(obj))

    @staticmethod
    def __setFieldService(appContext: AppContext):
        fieldService: FieldService = FieldService()
        fieldService.setAppContext(appContext)
        appContext.addService('fieldService', fieldService)

    @staticmethod
    def __setCommandService(appContext: AppContext):
        cmdService: CommandService = CommandService()
        cmdService.setAppContext(appContext)
        appContext.addService('commandService', cmdService)

    @staticmethod
    def __setMenuService(appContext: AppContext):
        menuService: MenuService = MenuService()
        menuService.setAppContext(appContext)
        appContext.addService('menuService', menuService)

    @staticmethod
    def __setTerminalService(screen, appContext: AppContext):
        terminalService = TerminalService(screen)
        terminalService.setAppContext(appContext)
        appContext.addService('terminalService', terminalService)
