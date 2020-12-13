from app_runner.menu.Command import Command

class Menu:
    _id: str
    _name: str
    _commands: dict
    _mid: str

    def __init__(self, id: str, name: str, mid: str):
        self._id = id
        self._name = name
        self._mid = mid
        self._commands = {}

    def getName(self) -> str:
        return self._name

    def setCommands(self, cmds: list):
        command: Command
        for command in cmds:
            self._commands[command.getId()] = command

    def addCommand(self, cmd: Command):
        self._commands[cmd.getId()] = cmd

    def getCommand(self, id: str) -> Command:
        return self._commands[id]

    def getCommandByIndex(self, index: int):
        cmds: list = list(self._commands.values())
        return cmds[index]

    def getCommands(self) -> dict:
        return self._commands

    def getCommandsAsList(self) -> list:
        return list(self._commands.values())

    def getCmdCount(self) -> int:
        return len(self._commands)

    def getModuleId(self) -> str:
        return self._mid

    def getId(self) -> int:
        return self._id

    def hasCommands(self) -> bool:
        return self.getCmdCount() > 0
