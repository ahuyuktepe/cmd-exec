
class Menu:
    _id: str
    _name: str
    _commands: list = []

    def __init__(self, id: str, name: str):
        self._id = id
        self._name = name

    def setCommands(self, cmds: list):
        self._commands = cmds
