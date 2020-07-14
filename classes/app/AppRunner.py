from classes.app.AppContext import AppContext
from classes.app.MainAppConfig import MainAppConfig
from classes.menu.Command import Command
from classes.services.ArgumentService import ArgumentService
from classes.services.CommandService import CommandService
from classes.services.FieldService import FieldService
from classes.services.LogService import LogService
from classes.services.MenuService import MenuService
from classes.utils.FileUtil import FileUtil
from classes.utils.ListUtil import ListUtil


class AppRunner:
    __argumentService: ArgumentService
    __appContext: AppContext
    __logService: LogService
    __menuService: MenuService
    __fieldService: FieldService
    __commandService: CommandService
    __fileService: FieldService

    def __init__(self, configPath: str):
        mainAppConfig = MainAppConfig(configPath)
        self.__appContext = AppContext(mainAppConfig)
        self.__argumentService = self.__appContext.getService('argumentService')
        self.__logService = self.__appContext.getService('logService')
        self.__menuService = self.__appContext.getService('menuService')
        self.__fieldService = self.__appContext.getService('fieldService')
        self.__commandService = self.__appContext.getService('commandService')

    def run(self):
        if self.__argumentService.isCmdMode():
            self.__runInCmdMode()
        elif self.__argumentService.isInteractiveMode():
            self.__runInInteractiveMode()

    def __runInCmdMode(self):
        try:
            print('Running in command mode')
            # 1) Fetch command identifiers
            mid: str = self.__argumentService.getMenuId()
            cid: str = self.__argumentService.getCmdId()
            # 2) Build command object
            menuFilePath: str = FileUtil.getMenuFilePath(mid)
            menuObj = FileUtil.generateObjFromYamlFile(menuFilePath)
            cmdObj: object = ListUtil.getElementByKey(menuObj.get('commands'), 'id', cid)
            cmd: Command = self.__commandService.buildCmd(cmdObj)
            # 3) Fetch field values
            fields: dict = cmd.getFields()
            fieldValues: dict = self.__argumentService.getArgsAsDict()
            # 4) Validate field values
            self.__fieldService.validateFieldValues(fields, fieldValues)
            # 5) Execute command
            self.__commandService.executeCommand(cmd)
        except Exception as exception:
            errDetails: str = str(exception)
            print(errDetails)
            self.__logService.error(errDetails)

    def __runInInteractiveMode(self):
        pass
