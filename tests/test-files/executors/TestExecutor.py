from cmd_exec.command.CmdExecutor import CmdExecutor
from cmd_exec.command.CmdRequest import CmdRequest
from cmd_exec.date.Date import Date


class TestExecutor(CmdExecutor):

    def run(self, request: CmdRequest):
        fields: dict = request.fields
        print('cls: TestExecutor, method: run')
        self.__printFields(fields)

    def testMethod(self, fields: dict):
        print('cls: TestExecutor, method: testMethod')
        self.__printFields(fields)

    def __printFields(self, fields: dict):
        if fields is not None:
            for fid, field in fields.items():
                value = field.getValue()
                if isinstance(value, Date):
                    print(fid + '=' + value.toString())
                elif isinstance(value, str):
                    print(fid + '=' + value)
