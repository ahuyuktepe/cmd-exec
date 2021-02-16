from src.app.CmdExecApp import CmdExecApp
from src.builder.AppContextBuilder import AppContextBuilder
from src.context.AppContext import AppContext
from src.context.AppContextManager import AppContextManager
from src.error.CmdExecError import CmdExecError
from src.service.ArgumentService import ArgumentService
from src.service.ConfigService import ConfigService
from src.util.ErrorUtil import ErrorUtil
from src.util.FileUtil import FileUtil
from src.util.ObjUtil import ObjUtil
from src.util.StrUtil import StrUtil
from src.util.ValidationUtil import ValidationUtil


class CmdExecAppRunner:

    @staticmethod
    def run():
        try:
            ObjUtil.initialize()
            FileUtil.initialize()
            ValidationUtil.failIfFileUtilIsNotInitialized()
            appContext = AppContextBuilder.buildBaseAppContext()
            app: CmdExecApp = CmdExecAppRunner.__buildCmdExecApp(appContext)
            app.run()
        except Exception as exp:
            ErrorUtil.handleException(exp)

    @staticmethod
    def __buildCmdExecApp(appContext: AppContext) -> CmdExecApp:
        # Get Services
        argService: ArgumentService = appContext.getService('argService')
        configService: ConfigService = appContext.getService('configService')
        # Init CmdExeApp object
        mid = argService.getMode()
        props = configService.getModePropsById(mid)
        clsPath = 'modules.{module}.src.app.{runner}'.format(**props)
        clsName = props.get('runner')
        # Validate
        ValidationUtil.failIfClassFileDoesNotExist(clsPath, 'ERR31', {'cls': clsName, 'path': clsPath})
        cls = StrUtil.convertClassNameStrToClass(clsPath, clsName)
        if not issubclass(cls, CmdExecApp):
            raise CmdExecError('ERR32', {'src': clsName, 'parent': 'CmdExecApp', 'name': props.get('module')})
        contextManager: AppContextManager = AppContextManager(appContext)
        app = ObjUtil.initClassFromStr(clsPath, clsName, [contextManager])
        return app
