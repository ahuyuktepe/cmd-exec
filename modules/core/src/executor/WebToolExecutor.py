from src.command.CmdExecutor import CmdExecutor
from src.field.FieldValues import FieldValues


class WebToolExecutor(CmdExecutor):

    def run(self, values: FieldValues):
        print('run method in WebToolExecutor')
        values.print()
