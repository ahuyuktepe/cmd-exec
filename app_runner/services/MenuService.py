from app_runner.menu.Command import Command
from app_runner.menu.Menu import Menu
from app_runner.services.BaseService import BaseService
from app_runner.services.FieldService import FieldService
from app_runner.utils.FileUtil import FileUtil


class MenuService(BaseService):

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

    def buildMenu(self, mid: str) -> Menu:
        menu: Menu = None
        if mid is not None:
            fileName = mid + '.yaml'
            filePath = FileUtil.getAbsolutePath(['resources', 'menus', fileName])
            if FileUtil.doesFileExist(filePath):
                menuProps = FileUtil.generateObjFromYamlFile(filePath)
                menu = Menu(
                    id=menuProps.get('id'),
                    name=menuProps.get('name'),
                    mid=menuProps.get('mid')
                )
                # Set commands
                commands: list = self.buildCommands(menuProps.get('commands'), mid)
                menu.setCommands(commands)
        return menu

    def buildCommands(self, cmds: list, mid: str) -> list:
        fieldService: FieldService = self._appContext.getService('fieldService')
        commands: list = []
        for cmdProps in cmds:
            command: Command = Command(
                id=cmdProps.get('id'),
                mid=mid,
                description=cmdProps.get('description')
            )
            command.setExecutor(cmdProps.get('executor'))
            command.setMenus(cmdProps.get('menus'))
            fields: list = fieldService.buildFields(cmdProps.get('fields'), mid)
            command.setFields(fields)
            commands.append(command)
        return commands
