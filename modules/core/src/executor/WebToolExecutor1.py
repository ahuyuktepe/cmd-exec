from src.command.CmdExecutor import CmdExecutor
from src.field.FieldValues import FieldValues


class WebToolExecutor1(CmdExecutor):

    def run(self, values: FieldValues):
        print('run method in WebToolExecutor1')
        values.print()
