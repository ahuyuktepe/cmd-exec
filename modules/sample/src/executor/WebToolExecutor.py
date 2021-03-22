from modules.sample.src.service.TestService import TestService
from src.classes.Option import Option
from src.command.CmdExecutor import CmdExecutor
from src.date.Date import Date
from src.field.DateField import DateField
from src.field.Field import Field
from src.field.SelectionField import SelectionField
from src.field.TextField import TextField
from src.service.ServiceType import ServiceType
from src.service.TerminalService import TerminalService


class WebToolExecutor(CmdExecutor):

    # def run(self, fields: dict):
    #     field: Field = fields.get('test_field')
    #     if field.isDate():
    #         date: Date = field.getValue()
    #         print('Date: ' + date.toString())
    #     elif field.isSelection():
    #         selectionField: SelectionField = field
    #         options = selectionField.getSelectedOptions()
    #         print('Selected Options: ' + str(options))
    #     else:
    #         value = field.getValue()
    #         print('Value: ' + str(value))
    #     service: TestService = self._contextManager.getService('testService')
    #     service.printAppName()

    def run(self, fields: dict):
        terminalService: TerminalService = self._contextManager.getService(ServiceType.TERMINAL_SERVICE)
        terminalService.print('#red#This #blue#is #green#a test #reset#message')
        # TextField
        field = TextField('f1')
        field.setLabel('Enter first name')
        terminalService.setFieldValueByUserInput(field)
        terminalService.print(field.getLabel() + ': ' + field.getValue())
        # Selection Field
        field = SelectionField('f2')
        field.setLabel('Select cities')
        options = [
            Option('ny', 'New York'),
            Option('ist', 'Istanbul'),
            Option('bst', 'Boston'),
            Option('ph', 'Philadelphia'),
            Option('ank', 'Ankara')
        ]
        field.appendOptions(options)
        terminalService.setFieldValueByUserInput(field)
        selectedOptions = field.getSelectedOptions()
        for option in selectedOptions:
            print(option.getValue())
        # DateField
        field = DateField('f3')
        field.setLabel('Enter #red#subscription date#reset#')
        terminalService.setFieldValueByUserInput(field)
        enteredDate = field.getValue()
        print('Date: ' + str(enteredDate.getValue()))
