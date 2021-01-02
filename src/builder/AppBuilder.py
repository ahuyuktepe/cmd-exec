from src.app.CmdExecApp import CmdExecApp
from src.builder.AppContextBuilder import AppContextBuilder
from src.utils.ErrorUtil import ErrorUtil
from src.utils.ValidationUtil import ValidationUtil


class AppBuilder:

    @staticmethod
    def build() -> CmdExecApp:
        try:
            ValidationUtil.failIfEnvironmentVarIsNotSet('APP_RUNNER_ROOT_PATH')
            appContext = AppContextBuilder.buildBaseAppContext()
            return CmdExecApp(appContext)
        except Exception as exp:
            ErrorUtil.handleException(exp)
        return CmdExecApp(None)
