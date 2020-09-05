from app_runner.app.config.AppConfig import AppConfig
from app_runner.app.context.AppContext import AppContext
from app_runner.app.context.AppContextBuilder import AppContextBuilder
from app_runner.app.runner.ApplicationRunner import ApplicationRunner
from app_runner.app.runner.CmdAppRunner import CmdAppRunner
from app_runner.app.runner.IntAppRunner import IntAppRunner

class AppRunnerFactory:

    @staticmethod
    def buildAppRunner() -> ApplicationRunner:
        appContext = AppContextBuilder.buildBaseAppContext()
        argumentService = appContext.getService('argumentService')
        if argumentService.isCmdMode():
            AppContextBuilder.updateContextForCommandMode(appContext)
            return AppRunnerFactory.__buildCmdRunner(appContext)
        elif argumentService.isInteractiveMode():
            AppContextBuilder.updateContextForInteractiveMode(appContext)
            return AppRunnerFactory.__buildInteractiveRunner(appContext)

    @staticmethod
    def __buildCmdRunner(appContext: AppContext) -> CmdAppRunner:
        return CmdAppRunner(appContext)

    @staticmethod
    def __buildInteractiveRunner(appContext: AppContext) -> IntAppRunner:
        return IntAppRunner(appContext)
