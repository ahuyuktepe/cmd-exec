from app_runner.app.context.AppContext import AppContext
from app_runner.app.runner.ApplicationRunner import ApplicationRunner
from app_runner.errors.FieldValidationErrors import FieldValidationErrors
from app_runner.menu.Command import Command
from app_runner.menu.Menu import Menu
from app_runner.utils.ErrorUtil import ErrorUtil


class CmdAppRunner(ApplicationRunner):

    def __init__(self, context: AppContext):
        super().__init__(context)

    def run(self):
        try:
            # 1) Get Command and Menu Id
            mid: str = self._argumentService.getMid()
            cid: str = self._argumentService.getCmd()
            # 2) Build Menu
            menu: Menu = self._menuService.buildMenu(mid)
            # 3) Get Command
            command: Command = menu.getCommand(cid)
            # 3) Fetch Arguments
            fieldValues: dict = self._fieldService.getFieldValues(command)
            # 4) Validate Values
            errors: FieldValidationErrors = self._fieldService.validateFieldValues(command, fieldValues)
            # 5) Call executor if no validation error
            if errors.hasErrors():
                errors.printErrors()
            else:
                self._commandService.execute(mid, command, fieldValues)
        except Exception as exception:
            ErrorUtil.handleException(exception, self._logService)
