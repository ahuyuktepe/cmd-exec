from app_runner.menu.Command import Command
from app_runner.services.BaseService import BaseService
from app_runner.utils.ObjUtil import ObjUtil
from app_runner.utils.ValidationUtil import ValidationUtil


class CommandService(BaseService):

    def execute(self, mid: str, cmd: Command, values: dict):
        clsName = cmd.getExecutorClass()
        ValidationUtil.failIfClassNotDefined(mid, clsName, 'executors')

        methodName: str = cmd.getExecutorMethod()
        package: str = 'modules.{module}.src.executors'.format(module=mid)
        classPath: str = package + "." + clsName
        cls = ObjUtil.getClassFromStr(package, clsName)
        executor = cls()
        ValidationUtil.failIfClassMethodDoesNotExist(executor, classPath, methodName)

        executor.setAppContext(self._appContext)
        method: object = getattr(executor, methodName)
        method(values)
