from app_runner.menu.Command import Command
from app_runner.services.BaseService import BaseService
from app_runner.utils.ErrorUtil import ErrorUtil
from app_runner.utils.FileUtil import FileUtil
from app_runner.utils.ListUtil import ListUtil
from app_runner.utils.ObjUtil import ObjUtil

class CommandService(BaseService):

    def buildCommand(self, cmdLocator: dict) -> Command:
        menuFilePath = FileUtil.getAbsolutePath(['modules', '{module}', 'menus', '{menu}.yaml'])
        menuFilePath = menuFilePath.format(**cmdLocator)
        if not FileUtil.doesFileExist(menuFilePath):
            raise FileNotFoundError("File in path '" + menuFilePath + "' does not exist.")
        menuObj = FileUtil.generateObjFromFile(menuFilePath)
        cmds: list = menuObj.get('commands')
        cmdProps = ListUtil.getElementByKey(cmds, 'id', cmdLocator['cid'])
        cmd: Command = Command(
            id=cmdProps.get('id'),
            description=cmdProps.get('description'),
            executor=cmdProps.get('executor'),
            module=cmdLocator.get('module')
        )
        self._appContext.getService('fieldService').insertFields(cmd, cmdProps.get('fields'))
        return cmd

    def execute(self, cmd: Command, values: dict):
        className = cmd.getExecutorClass()
        package: str = 'modules.{module}.src.executors'.format(module=cmd.getModule())
        cls = ObjUtil.getClassFromStr(package, className)
        executor = cls()
        executor.setAppContext(self._appContext)
        method: object = getattr(executor, cmd.getExecutorMethod())
        method(values)
