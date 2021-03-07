from modules.ui.src.service.TestService import TestService
from src.command.CmdExecutor import CmdExecutor
from src.date.Date import Date


class WebToolExecutor(CmdExecutor):

    def run(self, fields: dict):
        field = fields.get('publish_date')
        if field is not None:
            date: Date = field.getValue()
            print('Date: ' + date.toString())
        service: TestService = self._contextManager.getService('testService')
        service.printAppName()
