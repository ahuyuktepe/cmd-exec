from app_runner.app.AppConfig import AppConfig
from app_runner.app.AppContext import AppContext
from app_runner.errors.CmdExecError import CmdExecError
from app_runner.errors.FieldValidationErrors import FieldValidationErrors
from app_runner.menu.Command import Command
from app_runner.services.ArgumentService import ArgumentService
from app_runner.services.CommandService import CommandService
from app_runner.services.FieldService import FieldService
from app_runner.services.LogService import LogService
import traceback

class AppRunner:
    __argumentService: ArgumentService
    __appContext: AppContext
    __commandService: CommandService
    __fieldService: FieldService
    __logService: LogService

    def __init__(self, configPath: str):
        self.__argumentService = ArgumentService()
        self.__appContext = AppContext()
        self.__initializeDependencies()
        self.__commandService = self.__appContext.getService('commandService')
        self.__fieldService = self.__appContext.getService('fieldService')
        self.__logService = self.__appContext.getService('logService')

    def __initializeDependencies(self):
        config: AppConfig = self.__appContext.getConfig('main')
        # LogService
        obj: dict = config.getObjValue()
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
            # 1) Get command id
            cid: str = self.__argumentService.getCmdId()
            # 2) Get command locator
            appConfig: AppConfig = self.__appContext.getConfig('commands')
            cmdLocator: dict = appConfig.getObjValue(cid)
            # 3) Build Command object
            cmd: Command = self.__commandService.buildCommand(cid, cmdLocator)
            # 4) Fetch arguments
            fieldValues: dict = self.__fieldService.getFieldValues(cmd)
            # 5) Validate values
            errors: FieldValidationErrors = self.__fieldService.validateFieldValues(cmd, fieldValues)
            # 6) Call executor if no validation error
            if errors.hasErrors():
                errors.printErrors()
            else:
                self.__commandService.execute(cmd, fieldValues)
        except CmdExecError as cmdExecError:
            print('\033[31mCmdExecError : ' + str(cmdExecError) + '\033[0m')
            self.__logService.error(str(cmdExecError))
        except Exception as exception:
            errorDetails: str = traceback.format_exc()
            self.__logService.error(errorDetails)
            print(errorDetails)

    def __runInInteractiveMode(self):
        pass
