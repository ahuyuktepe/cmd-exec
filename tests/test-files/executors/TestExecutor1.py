from cmd_exec.command.CmdExecutor import CmdExecutor
from cmd_exec.command.CmdRequest import CmdRequest


class TestExecutor1(CmdExecutor):

    def run(self, request: CmdRequest):
        print('Running TestExecutor1')
