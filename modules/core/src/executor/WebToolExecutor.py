from src.command.CmdExecutor import CmdExecutor


class WebToolExecutor(CmdExecutor):

    def run(self, fields: dict):
        print('run method in WebToolExecutor')
        for fid, field in fields.items():
            field.print()
