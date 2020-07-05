from classes.menu.Command import Command
from classes.menu.Menu import Menu

class MenuService:

    def buildMenu(self, obj: dict) -> Menu:
        menu = Menu(
            id=obj.get('id'),
            name=obj.get('name')
        )
        cmdObjList = obj.get('commands')
        commands = self.__getCommandsFromCommandObjects(cmdObjList)
        menu.setCommands(commands)
        return menu

    def __getCommandsFromCommandObjects(self, cmdObjects: list) -> list:
        commands: list = []
        if commands is not None:
            for cmdObj in cmdObjects:
                commands.append(Command(
                    id=cmdObj.get('id'),
                    description=cmdObj.get('description'),
                    executor=cmdObj.get('executor')
                ))
        return commands
