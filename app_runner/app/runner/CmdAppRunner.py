from app_runner.app.context.AppContext import AppContext
from app_runner.app.runner.ApplicationRunner import ApplicationRunner
from app_runner.errors.FieldValidationErrors import FieldValidationErrors
from app_runner.menu.Command import Command
from app_runner.menu.Menu import Menu
from app_runner.utils.ErrorUtil import ErrorUtil
from app_runner.utils.StrUtil import StrUtil


class CmdAppRunner(ApplicationRunner):

    def __init__(self, context: AppContext):
        super().__init__(context)

    def run(self):
        try:
            # 1) Get Command and Menu Id
            menuId: str = self._argumentService.getMenu()
            cid: str = self._argumentService.getCmd()
            if StrUtil.isNoneOrEmpty(menuId) or StrUtil.isNoneOrEmpty(cid):
                raise Exception('Target command can not be found.')
            # 2) Build Menu
            menu: Menu = self._menuService.buildMenu(menuId)
            # 3) Get Command
            command: Command = menu.getCommand(cid)
            if command is None:
                msg = "Command '{cmd}' does not exist in menu '{menu}'.".format(cmd=cid, menu=menu.getName())
                raise Exception(msg)
            # 4) Fetch Arguments
            fieldValues: dict = self._fieldService.getFieldValues(command)
            # 5) Validate Values
            errors: FieldValidationErrors = self._fieldService.validateFieldValues(command, fieldValues)
            # 6) Call executor if no validation error
            if errors.hasErrors():
                errors.printErrors()
            else:
                self._commandService.execute(command, fieldValues)
        except Exception as exception:
            ErrorUtil.handleException(exception, self._logService)
