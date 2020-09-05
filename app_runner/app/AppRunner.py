from app_runner.app.AppConfig import AppConfig
from app_runner.app.AppContext import AppContext
from app_runner.errors.FieldValidationErrors import FieldValidationErrors
from app_runner.menu.Command import Command
from app_runner.services.ArgumentService import ArgumentService
from app_runner.services.CommandService import CommandService
from app_runner.services.FieldService import FieldService
from app_runner.services.LogService import LogService
from app_runner.utils.ErrorUtil import ErrorUtil


class AppRunner:
    __argumentService: ArgumentService
    __appContext: AppContext
    __commandService: CommandService
    __fieldService: FieldService
    __logService: LogService

    def __init__(self):
        self.__argumentService = ArgumentService()
        self.__appContext = AppContext()
        self.__initializeDependencies()
        self.__commandService = self.__appContext.getService('commandService')
        self.__fieldService = self.__appContext.getService('fieldService')
        self.__logService = self.__appContext.getService('logService')

    def __initializeDependencies(self):
        config: AppConfig = self.__appContext.getConfig('main')
        # LogService
        obj: dict = config.getObjValue('log_settings')
        self.__appContext.addService('logService', LogService(obj))
        # FieldService
        fieldService: FieldService = FieldService()
        fieldService.setAppContext(self.__appContext)
        self.__appContext.addService('fieldService', fieldService)
        # CommandService
        cmdService: CommandService = CommandService()
        cmdService.setAppContext(self.__appContext)
        self.__appContext.addService('commandService', cmdService)
        # ArgumentService
        self.__argumentService.setAppContext(self.__appContext)
        self.__appContext.addService('argumentService', self.__argumentService)

    def run(self):
        if self.__argumentService.isCmdMode():
            self.__runInCmdMode()
        elif self.__argumentService.isInteractiveMode():
            self.__runInInteractiveMode()

    def __runInCmdMode(self):
        try:
            # 1) Set command locator
            cid: str = self.__argumentService.getCmd()
            appConfig: AppConfig = self.__appContext.getConfig('main')
            cmdLocator: dict = appConfig.getObjValue('command_locators.' + cid)
            # 2) Build Command object
            cmd: Command = self.__commandService.buildCommand(cmdLocator)
            # 3) Fetch arguments
            fieldValues: dict = self.__fieldService.getFieldValues(cmd)
            # 4) Validate values
            errors: FieldValidationErrors = self.__fieldService.validateFieldValues(cmd, fieldValues)
            # 5) Call executor if no validation error
            if errors.hasErrors():
                errors.printErrors()
            else:
                self.__commandService.execute(cmd, fieldValues)
        except Exception as exception:
            ErrorUtil.handleException(exception, self.__logService)

    def __runInInteractiveMode(self):
        pass
