from src.command.CmdExecutor import CmdExecutor


class WebToolExecutor1(CmdExecutor):

    def run(self, fields: dict):
        print('run method in WebToolExecutor1')
