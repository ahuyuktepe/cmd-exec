from app_runner.app.config.AppConfig import AppConfig
from app_runner.app.context.AppContext import AppContext
from app_runner.services.ArgumentService import ArgumentService
from app_runner.services.CommandService import CommandService
from app_runner.services.FieldService import FieldService
from app_runner.services.LogService import LogService
from app_runner.services.MenuService import MenuService
from app_runner.services.UIService import UIService
from app_runner.utils.UIPrintAreaUtil import UIPrintAreaUtil
from app_runner.ui_elements.UIScreen import UIScreen
from app_runner.enums.UIColor import UIColor


class AppContextBuilder:

    @staticmethod
    def updateContextForInteractiveMode(appContext: AppContext):
        AppContextBuilder.__setTerminalService(appContext)
        UIPrintAreaUtil.initializeScreen()
        UIColor.setColorCodes()

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
    def __setArgumentService(appContext: AppContext):
        appContext.addService('argumentService', ArgumentService())

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

    @staticmethod
    def __setTerminalService(appContext: AppContext):
        uiService = UIService()
        uiService.setAppContext(appContext)
        screen = UIScreen(appContext)
        uiService.setScreen(screen)
        # Add Service
        appContext.addService('uiService', uiService)
