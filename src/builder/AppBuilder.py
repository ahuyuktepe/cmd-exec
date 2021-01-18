from src.app.CmdExecApp import CmdExecApp
from src.builder.AppContextBuilder import AppContextBuilder
from src.util.ErrorUtil import ErrorUtil
from src.util.ValidationUtil import ValidationUtil


class AppBuilder:

    @staticmethod
    def build() -> CmdExecApp:
        try:
            ValidationUtil.failIfEnvironmentVarIsNotValid('APP_RUNNER_ROOT_PATH')
            appContext = AppContextBuilder.buildBaseAppContext()
            return CmdExecApp(appContext)
        except Exception as exp:
            ErrorUtil.handleException(exp)
            exit(1)
