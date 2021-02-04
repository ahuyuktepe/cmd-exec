from src.field.FieldValues import FieldValues
from src.menu.Command import Command
from src.service.AppService import AppService


class CommandService(AppService):

    def buildCmdFromId(self, cid: str) -> Command:
        pass

    def execute(self, cmd: Command):
        values = FieldValues()
        values.addValue('id', 'This is the id of element')

