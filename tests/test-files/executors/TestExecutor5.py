from cmd_exec.command.CmdExecutor import CmdExecutor
from cmd_exec.command.CmdRequest import CmdRequest


class TestExecutor5(CmdExecutor):

    def testMethod(self, request: CmdRequest):
        print('Running TestExecutor5')
        fields: dict = request.fields
        if fields is not None:
            for fid, field in fields.items():
                if field.isDate():
                    value = field.getValue()
                    print(fid + '=' + value.toString())
                elif field.isSelection():
                    options: list = field.getOptions()
                    for option in options:
                       print('foid > ' + option.getId() + ': ' + option.getValue())
                    options = field.getSelectedOptions()
                    for option in options:
                        print('soid > ' + option.getId() + ': ' + option.getValue())
