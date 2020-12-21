from app_runner.app.context.AppContext import AppContext
from app_runner.app.context.AppContextBuilder import AppContextBuilder
from app_runner.app.runner.ApplicationRunner import ApplicationRunner
from app_runner.app.runner.CmdAppRunner import CmdAppRunner
from app_runner.app.runner.IntAppRunner import IntAppRunner
from app_runner.services.ArgumentService import ArgumentService
from app_runner.utils.ErrorUtil import ErrorUtil
from app_runner.utils.ValidationUtil import ValidationUtil


class AppRunnerFactory:

    @staticmethod
    def buildAppRunner() -> ApplicationRunner:
        try:
            ValidationUtil.failIfEnvironmentVarIsNotSet('APP_RUNNER_ROOT_PATH')
            appContext = AppContextBuilder.buildBaseAppContext()
            argumentService: ArgumentService = appContext.getService('argumentService')
            if argumentService.isCmdMode():
                AppContextBuilder.updateContextForCommandMode(appContext)
                return AppRunnerFactory.__buildCmdRunner(appContext)
            elif argumentService.isInteractiveMode():
                AppContextBuilder.updateContextForInteractiveMode(appContext)
                return AppRunnerFactory.__buildInteractiveRunner(appContext)
        except Exception as exp:
            ErrorUtil.handleException(exp)

    @staticmethod
    def __buildCmdRunner(appContext: AppContext) -> ApplicationRunner:
        return CmdAppRunner(appContext)

    @staticmethod
    def __buildInteractiveRunner(appContext: AppContext) -> ApplicationRunner:
        return IntAppRunner(appContext)
