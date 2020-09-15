from app_runner.menu.Command import Command
from app_runner.services.BaseService import BaseService
from app_runner.utils.FileUtil import FileUtil
from app_runner.utils.ListUtil import ListUtil
from app_runner.utils.ObjUtil import ObjUtil
from app_runner.utils.ValidationUtil import ValidationUtil


class CommandService(BaseService):

    def buildCommand(self, cmdLocator: dict) -> Command:
        ValidationUtil.failIfObjNone(cmdLocator, 'Command locator is None.')
        menuFilePath = FileUtil.getAbsolutePath(['modules', '{module}', 'menus', '{menu}.yaml'])
        menuFilePath = menuFilePath.format(**cmdLocator)
        ValidationUtil.failIfFileNotReadable(menuFilePath)
        menuObj = FileUtil.generateObjFromFile(menuFilePath)
        ValidationUtil.failIfObjNone(menuObj, 'Menu object is None.')
        cmds: list = menuObj.get('commands')
        ValidationUtil.failIfObjNone(cmds, "The menu file '"+menuFilePath+"' does not contain commands key.")
        cmdProps = ListUtil.getElementByKey(cmds, 'id', cmdLocator.get('cmd'))
        ValidationUtil.validateCmdProps(cmdProps)
        cmd: Command = Command(
            id=cmdProps.get('id'),
            description=cmdProps.get('description'),
            executor=cmdProps.get('executor'),
            module=cmdLocator.get('module')
        )
        self._appContext.getService('fieldService').insertFields(cmd, cmdProps.get('fields'))
        return cmd

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
