from cmd_exec.command.CmdExecutor import CmdExecutor
from cmd_exec.command.CmdRequest import CmdRequest
from cmd_exec.date.Date import Date


class TestExecutor4(CmdExecutor):

    def run(self, request: CmdRequest):
        print('Running TestExecutor4')
        fields: dict = request.fields
        if fields is not None:
            for fid, field in fields.items():
                value = field.getValue()
                if isinstance(value, Date):
                    print(fid + '=' + value.toString())
