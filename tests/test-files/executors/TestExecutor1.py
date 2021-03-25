from command.CmdExecutor import CmdExecutor


class TestExecutor1(CmdExecutor):

    def run(self, fields: dict):
        print('Running TestExecutor1')
