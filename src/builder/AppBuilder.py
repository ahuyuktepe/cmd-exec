from src.app.CmdExecApp import CmdExecApp
from src.builder.AppContextBuilder import AppContextBuilder
<<<<<<< HEAD
from src.utils.ErrorUtil import ErrorUtil
from src.utils.ValidationUtil import ValidationUtil
=======
from src.util.ErrorUtil import ErrorUtil
from src.util.ValidationUtil import ValidationUtil
>>>>>>> refactoring


class AppBuilder:

    @staticmethod
    def build() -> CmdExecApp:
        try:
<<<<<<< HEAD
            ValidationUtil.failIfEnvironmentVarIsNotSet('APP_RUNNER_ROOT_PATH')
=======
            ValidationUtil.failIfEnvironmentVarIsNotValid('APP_RUNNER_ROOT_PATH')
>>>>>>> refactoring
            appContext = AppContextBuilder.buildBaseAppContext()
            return CmdExecApp(appContext)
        except Exception as exp:
            ErrorUtil.handleException(exp)
<<<<<<< HEAD
        return CmdExecApp(None)
=======
            exit(1)
>>>>>>> refactoring
