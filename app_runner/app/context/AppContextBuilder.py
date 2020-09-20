from app_runner.app.config.AppConfig import AppConfig
from app_runner.app.context.AppContext import AppContext
from app_runner.services.ArgumentService import ArgumentService
from app_runner.services.CommandService import CommandService
from app_runner.services.FieldService import FieldService
from app_runner.services.LogService import LogService
from app_runner.services.MenuService import MenuService
from app_runner.services.ScreenService import ScreenService
from app_runner.ui.terminal.element.UIScreen import UIScreen


class AppContextBuilder:

    @staticmethod
    def updateContextForInteractiveMode(appContext: AppContext):
        AppContextBuilder.__setScreenService(appContext)
        AppContextBuilder.__setScreen(appContext)

    @staticmethod
    def updateContextForCommandMode(appContext: AppContext):
        pass

    @staticmethod
    def buildBaseAppContext() -> AppContext:
        appContext = AppContext()
        appContext.initializeConfig('main')
        AppContextBuilder.__setArgumentService(appContext)
        AppContextBuilder.__setLogService(appContext)
        AppContextBuilder.__setFieldService(appContext)
        AppContextBuilder.__setCommandService(appContext)
        AppContextBuilder.__setMenuService(appContext)
        return appContext

    @staticmethod
    def __setScreen(appContext: AppContext):
        screen = UIScreen()
        appContext.setScreen(screen)

    @staticmethod
    def __setArgumentService(appContext: AppContext):
        appContext.addService('argumentService', ArgumentService())

    @staticmethod
    def __setScreenService(appContext: AppContext):
        appContext.addService('screenService', ScreenService())

    @staticmethod
    def __setLogService(appContext: AppContext):
        config: AppConfig = appContext.getConfig('main')
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
