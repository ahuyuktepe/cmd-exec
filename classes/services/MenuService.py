from classes.menu.Menu import Menu
from classes.services.CommandService import CommandService

class MenuService:
    __cmdService: CommandService

    def setCmdService(self, cmdService: CommandService):
        self.__cmdService = cmdService

    def buildMenu(self, obj: dict) -> Menu:
        menu = Menu(
            id=obj.get('id'),
            name=obj.get('name')
        )
        cmdObjList = obj.get('commands')
        commands = self.__cmdService.getCommands(cmdObjList)
        menu.setCommands(commands)
        return menu
