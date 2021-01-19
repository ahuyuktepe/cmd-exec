from src.app.CmdExecApp import CmdExecApp
from src.builder.AppContextBuilder import AppContextBuilder
from src.context.AppContext import AppContext
from src.context.AppContextManager import AppContextManager
from src.service.ArgumentService import ArgumentService
from src.service.ConfigService import ConfigService
from src.util.ErrorUtil import ErrorUtil
from src.util.ObjUtil import ObjUtil
from src.util.ValidationUtil import ValidationUtil


class AppBuilder:

    @staticmethod
    def build() -> CmdExecApp:
        try:
            ValidationUtil.failIfEnvironmentVarIsNotValid('APP_RUNNER_ROOT_PATH')
            appContext = AppContextBuilder.buildBaseAppContext()
            return AppBuilder.__buildCmdExecApp(appContext)
        except Exception as exp:
            ErrorUtil.handleException(exp)
            exit(1)

    @staticmethod
    def __buildCmdExecApp(appContext: AppContext) -> CmdExecApp:
        # Get Services
        argService: ArgumentService = appContext.getService('argService')
        configService: ConfigService = appContext.getService('configService')
        # Init CmdExeApp object
        mid = argService.getMode()
        props = configService.getModePropsById(mid)
        clsPath = 'modules.{module}.src.app.{runner}'.format(**props)
        cls = props.get('runner')
        contextManager: AppContextManager = AppContextManager(appContext)
        runner = ObjUtil.initClassFromStr(clsPath, cls, [contextManager])
        return runner
