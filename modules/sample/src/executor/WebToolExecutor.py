from modules.sample.src.service.TestService import TestService
from src.command.CmdExecutor import CmdExecutor
from src.date.Date import Date
from src.field.Field import Field
from src.field.SelectionField import SelectionField


class WebToolExecutor(CmdExecutor):

    def run(self, fields: dict):
        field: Field = fields.get('test_field')
        if field.isDate():
            date: Date = field.getValue()
            print('Date: ' + date.toString())
        elif field.isSelection():
            selectionField: SelectionField = field
            options = selectionField.getSelectedOptions()
            print('Selected Options: ' + str(options))
        else:
            value = field.getValue()
            print('Value: ' + str(value))
        service: TestService = self._contextManager.getService('testService')
        service.printAppName()
