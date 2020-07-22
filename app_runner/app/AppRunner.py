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
            mid: str = self.__argumentService.getMenuId()
            cid: str = self.__argumentService.getCmdId()
            # 1) Setup menu file path
            menuFilePath = FileUtil.getAbsolutePath(['modules', 'sample', 'menus', '{mid}.yaml']).format(mid=mid)
            # 2) Read menu file content into object
            menuObj = FileUtil.generateObjFromFile(menuFilePath)
            # 3) Get command object
            cmds: list = menuObj.get('commands')
            cmdObj = ListUtil.getElementByKey(cmds, 'id', cid)
            # 4) Build command object
            cmd: Command = self.__commandService.buildCmd(cmdObj)
            # 6) Insert fields
            self.__fieldService.insertFields(cmd, cmdObj.get('fields'))
            # 7) Fetch field values
            fields: dict = cmd.getFields()
            fieldValues: dict = self.__argumentService.getArgsAsDict()
            # 8) Import default values
            fieldValues = self.__commandService.getValuesWithDefaultValues(fieldValues, cmd)
            # 9) Validate field values
            self.__fieldService.validateFieldValues(fields, fieldValues)
            # 10) Initialize executor class
            executor = self.__commandService.initializeExecutorClass(cmd.getExecutorClass())
            executor.setAppContext(self.__appContext)
            # 11) Call executor method
            self.__commandService.callExecutorMethod(executor, cmd.getExecutorMethod(), fieldValues)
        except Exception as exception:
            errorDetails: str = traceback.format_exc()
            self.__logService.error(errorDetails)
            print(errorDetails)

    def __runInInteractiveMode(self):
        pass
