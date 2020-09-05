from app_runner.app.config.AppConfig import AppConfig
from app_runner.app.context.AppContext import AppContext
from app_runner.menu.Command import Command
from app_runner.services.ArgumentService import ArgumentService
from app_runner.services.CommandService import CommandService
from app_runner.services.FieldService import FieldService
from app_runner.services.LogService import LogService


class ApplicationRunner:
    _argumentService: ArgumentService
    _appContext: AppContext
    _commandService: CommandService
    _fieldService: FieldService
    _logService: LogService

    def __init__(self, context: AppContext):
        self._appContext = context
        self._commandService = self._appContext.getService('commandService')
        self._fieldService = self._appContext.getService('fieldService')
        self._logService = self._appContext.getService('logService')
        self._argumentService = self._appContext.getService('argumentService')

    def run(self):
        print('Running application')

    def _getCommand(self, cid: str) -> Command:
        # Get command locator
        appConfig: AppConfig = self._appContext.getConfig('main')
        cmdLocator: dict = appConfig.getObjValue('command_locators.' + cid)
        # Build command
        cmd: Command = self._commandService.buildCommand(cmdLocator)
        return cmd
