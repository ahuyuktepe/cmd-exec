from app_runner.menu.Command import Command
from app_runner.services.BaseService import BaseService
from app_runner.utils.FileUtil import FileUtil
from app_runner.utils.ObjUtil import ObjUtil
from app_runner.utils.StrUtil import StrUtil
from app_runner.utils.ValidationUtil import ValidationUtil


class CommandService(BaseService):

    # Utility Methods

    def execute(self, cmd: Command, values: dict):
        if cmd.hasExecutor():
            executorPath = cmd.getExecutor()
            props = StrUtil.getClassMethodMapFromStr(executorPath, 'execute')
            mid: str = props['module']
            clsName = props['class']
            FileUtil.failIfClassFileDoesNotExist(mid, clsName, 'executors')

            methodName: str = props['method']
            classPath: str = 'modules.{module}.src.executors.{className}'.format(module=mid, className=clsName)
            cls = ObjUtil.getClassFromStr(classPath, clsName)
            executor = cls()
            ValidationUtil.failIfClassMethodDoesNotExist(executor, classPath, methodName)

            executor.setAppContext(self._appContext)
            method: object = getattr(executor, methodName)
            method(values)
