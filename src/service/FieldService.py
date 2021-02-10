from src.field.Field import Field
from src.menu.Command import Command
from src.service.AppService import AppService


class FieldService(AppService):

    def buildField(self, cid: str, props: dict) -> Field:
        pass

    def getFieldValuesFromArgumentFile(self, cmd: Command) -> dict:
        pass

    def getFieldValuesFromCmdArgs(self, cmd: Command) -> dict:
        pass

    def getFieldValuesFromUser(self, cmd: Command) -> dict:
        pass
