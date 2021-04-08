from cmd_exec.field.Field import Field
from cmd_exec.service.AppService import AppService


class TerminalService(AppService):

    def print(self, text: str, model: dict = {}):
        pass

    def getFieldValue(self, field: Field):
        pass

    def getFieldValues(self, fields: list):
        pass
