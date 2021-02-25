from src.command.CmdExecutor import CmdExecutor
from src.date.Date import Date


class TestExecutor(CmdExecutor):

    def run(self, fields: dict):
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