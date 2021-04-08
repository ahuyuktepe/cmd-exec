from cmd_exec.command.CmdExecutor import CmdExecutor
from cmd_exec.field.Field import Field
from cmd_exec.service.LogService import LogService
from cmd_exec.service.ServiceType import ServiceType


class SampleCmdExecutor(CmdExecutor):

    def runCommand(self, fields: dict):
        print("running command")
        service: LogService = self._contextManager.getService(ServiceType.LOG_SERVICE)
        service.info("This is a test message")
        service = self._contextManager.getService('sampleService')
        service.printAppName()
        field: Field = fields.get('first_name')
        field.print()
        print("Value: " + field.getValue())

