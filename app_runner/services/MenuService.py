from app_runner.menu.Command import Command
from app_runner.menu.Menu import Menu
from app_runner.services.BaseService import BaseService
from app_runner.services.FieldService import FieldService
from app_runner.utils.FileUtil import FileUtil
from app_runner.utils.StrUtil import StrUtil


class MenuService(BaseService):

    # Utility Methods

    def buildMenus(self, mids: list) -> list:
        if mids is None:
            return None
        menus: list = []
        for mid in mids:
            menu = self.buildMenu(mid)
            if menu is not None:
                menus.append(menu)
        return menus

    def buildMenusFromCommaSeparatedIds(self, menuIdsStr: str) -> list:
        if menuIdsStr is None:
            return []
        menuIds: list = menuIdsStr.split(',')
        return self.buildMenus(menuIds)

    def buildMenu(self, menuId: str) -> Menu:
        menu: Menu = None
        if menuId is not None:
            fileName = menuId + '.yaml'
            filePath = FileUtil.getAbsolutePath(['resources', 'menus', fileName])
            if FileUtil.doesFileExist(filePath):
                menuProps = FileUtil.generateObjFromYamlFile(filePath)
                menu = Menu(
                    id=menuProps.get('id'),
                    name=menuProps.get('name'),
                    module=menuProps.get('module')
                )
                # Set commands
                commands: list = self.buildCommands(menuProps.get('commands'), menuId)
                menu.setCommands(commands)
            else:
                raise Exception("Menu file '{filePath}' does not exist.".format(filePath=filePath))
        return menu

    def buildCommands(self, cmds: list, module: str) -> list:
        fieldService: FieldService = self._appContext.getService('fieldService')
        commands: list = []
        for cmdProps in cmds:
            command: Command = Command(
                id=cmdProps.get('id'),
                description=cmdProps.get('description')
            )
            executorPath = StrUtil.prependModule(cmdProps.get('executor'), module)
            command.setExecutor(executorPath)
            command.setMenus(cmdProps.get('menus'))
            fields: list = fieldService.buildFields(module, cmdProps.get('fields'))
            command.setFields(fields)
            commands.append(command)
        return commands
