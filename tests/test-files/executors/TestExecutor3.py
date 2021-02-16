from src.command.CmdExecutor import CmdExecutor
from src.date.Date import Date


class TestExecutor3(CmdExecutor):

    def run(self, fields: dict):
        print('Running TestExecutor3')
        if fields is not None:
            for fid, field in fields.items():
                value = field.getValue()
                if isinstance(value, Date):
                    print(fid + '=' + value.toString())
