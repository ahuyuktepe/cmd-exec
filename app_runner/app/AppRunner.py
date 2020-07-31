from app_runner.app.AppContext import AppContext
from app_runner.app.MainAppConfig import MainAppConfig
from app_runner.menu.Command import Command
from app_runner.services.ArgumentService import ArgumentService
from app_runner.services.CommandService import CommandService
from app_runner.services.FieldService import FieldService
from app_runner.services.LogService import LogService
import traceback
from app_runner.utils.FileUtil import FileUtil
from app_runner.utils.ListUtil import ListUtil
from modules.main.src.executors.WebToolExecutor import WebToolExecutor


class AppRunner:
    __argumentService: ArgumentService
    __appContext: AppContext
    __commandService: CommandService
    __fieldService: FieldService
    __logService: LogService

    def __init__(self, configPath: str):
        self.__argumentService = ArgumentService()
        self.__initializeAppContext(configPath)
        self.__initializeDependencies()
        self.__commandService = self.__appContext.getService('commandService')
        self.__fieldService = self.__appContext.getService('fieldService')
        self.__logService = self.__appContext.getService('logService')

    def __initializeAppContext(self, configPath: str):
        props = FileUtil.generateObjFromYamlFile(configPath)
        mainAppConfig = MainAppConfig(props)
        self.__appContext = AppContext(mainAppConfig)

    def __initializeDependencies(self):
        # LogService
        obj: dict = self.__appContext.getConfig('main').getObjValue('log_settings')
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
            # 1) Get comman
            # d id
            cid: str = self.__argumentService.getCmdId()
            # 2) Get command locator
            mainConfig: MainAppConfig = self.__appContext.getConfig('main')
            cmdLocator: dict = mainConfig.getCommandLocator(cid)
            # 3) Build Command object
            cmd: Command = self.__commandService.buildCommand(cmdLocator)
            # 4) Fetch arguments
            fieldValues: dict = self.__fieldService.getFieldValues(cmd)
            # 5) Validate values
            self.__fieldService.validateFieldValues(cmd, fieldValues)
            # 6) Call executor if set
            self.__commandService.execute(cmd, fieldValues)
        except Exception as exception:
            errorDetails: str = traceback.format_exc()
            self.__logService.error(errorDetails)
            print(errorDetails)

    def __runInInteractiveMode(self):
        pass
