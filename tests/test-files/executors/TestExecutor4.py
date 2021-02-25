from src.command.CmdExecutor import CmdExecutor
from src.date.Date import Date


class TestExecutor4(CmdExecutor):

    def run(self, fields: dict):
        print('Running TestExecutor4')
        if fields is not None:
            for fid, field in fields.items():
                value = field.getValue()
                if isinstance(value, Date):
                    print(fid + '=' + value.toString())
