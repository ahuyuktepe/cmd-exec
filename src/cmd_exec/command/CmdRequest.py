from ..field.Field import Field
from ..service.TerminalService import TerminalService


class CmdRequest:
    fields: dict
    flags: list
    terminalService: TerminalService

    def __init__(self, service: TerminalService, fields: dict, flags: list):
        self.fields = fields
        self.terminalService = service
        self.flags = flags

    def getField(self, fid: str) -> Field:
        if self.hasField(fid):
            return self.fields[fid]
        return None

    def hasField(self, fid: str) -> bool:
        return self.fields is not None and fid in self.fields.keys()

    def getFieldValue(self, fid: str) -> object:
        field: Field = self.getField(fid)
        if field is not None:
            return field.getValue()
        return None

    def getFieldValueAsStr(self, fid: str) -> str:
        return str(self.getFieldValue(fid))

    def hasFlag(self, flag: str):
        return flag in self.flags


