from app_runner.app.context.AppContext import AppContext
from app_runner.app.runner.ApplicationRunner import ApplicationRunner
from app_runner.errors.FieldValidationErrors import FieldValidationErrors
from app_runner.menu.Command import Command
from app_runner.utils.ErrorUtil import ErrorUtil


class CmdAppRunner(ApplicationRunner):

    def __init__(self, context: AppContext):
        super().__init__(context)

    def run(self):
        try:
            print('running in cmd mode')
            # 1) Get command id
            cid: str = self._argumentService.getCmd()
            # 2) Build Command object
            cmd: Command = self._getCommand(cid)
            # 3) Fetch arguments
            fieldValues: dict = self._fieldService.getFieldValues(cmd)
            # 4) Validate values
            errors: FieldValidationErrors = self._fieldService.validateFieldValues(cmd, fieldValues)
            # 5) Call executor if no validation error
            if errors.hasErrors():
                errors.printErrors()
            else:
                self._commandService.execute(cmd, fieldValues)
        except Exception as exception:
            ErrorUtil.handleException(exception, self._logService)
