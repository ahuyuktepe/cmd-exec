from app_runner.menu.Command import Command

class Menu:
    _id: str
    _name: str
    _commands: dict

    def __init__(self, id: str, name: str):
        self._id = id
        self._name = name

    def setCommands(self, cmds: dict):
        self._commands = cmds

    def getCommand(self, id: str) -> Command:
        return self._commands[id]
