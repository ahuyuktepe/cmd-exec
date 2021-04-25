import os
import sys
from cmd_exec.app.CmdExecApp import CmdExecApp
from cmd_exec.builder.AppContextBuilder import AppContextBuilder
from cmd_exec.context.AppContext import AppContext
from cmd_exec.context.AppContextManager import AppContextManager
from cmd_exec.error.CmdExecError import CmdExecError
from cmd_exec.service.ArgumentService import ArgumentService
from cmd_exec.service.ConfigurationService import ConfigurationService
from cmd_exec.util.ErrorUtil import ErrorUtil
from cmd_exec.util.FileUtil import FileUtil
from cmd_exec.util.ObjUtil import ObjUtil
from cmd_exec.util.ValidationUtil import ValidationUtil


class CmdExecAppRunner:
    __rootPath: str = None

    @staticmethod
    def run(env: str = 'production'):
        try:
            CmdExecAppRunner.__setRootDir(env)
            FileUtil.setRootPath(CmdExecAppRunner.__rootPath)
            sys.path.append(CmdExecAppRunner.__rootPath)
            appContext = AppContextBuilder.buildBaseAppContext()
            app: CmdExecApp = CmdExecAppRunner.__buildCmdExecApp(appContext)
            app.run()
        except Exception as exp:
            ErrorUtil.handleException(exp)

    @staticmethod
    def __setRootDir(env: str):
        if CmdExecAppRunner.__rootPath is None:
            rootPath = os.environ['APP_RUNNER_ROOT_PATH']
            if env == 'test':
                rootPath = os.path.sep.join([rootPath, 'tests', 'target'])
            CmdExecAppRunner.__rootPath = rootPath

    @staticmethod
    def __buildCmdExecApp(appContext: AppContext) -> CmdExecApp:
        # Get Services
        argService: ArgumentService = appContext.getService('argService')
        configService: ConfigurationService = appContext.getService('configService')
        # Init CmdExeApp object
        mid = argService.getMode()
        props = configService.getModePropsById(mid)
        module = props.get('module')
        clsName = props.get('runner')
        if module is None:
            clsPath = 'cmd_exec.app.{runner}'.format(**props)
        else:
            clsPath = 'modules.{module}.src.app.{runner}'.format(**props)
            # Validate
            ValidationUtil.failIfClassFileDoesNotExist(clsPath, 'ERR31', {'cls': clsName, 'path': clsPath})
        cls = ObjUtil.getClassFromClsPath(clsPath, clsName)
        if not issubclass(cls, CmdExecApp):
            raise CmdExecError('ERR32', {'src': clsName, 'parent': 'CmdExecApp', 'name': props.get('module')})
        contextManager: AppContextManager = AppContextManager(appContext)
        app = ObjUtil.initClassFromStr(clsPath, clsName, [contextManager])
        return app
