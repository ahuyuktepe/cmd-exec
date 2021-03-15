from src.action.CmdAction import CmdAction
from src.action.CmdActionResponse import CmdActionResponse
from src.menu.Command import Command


class TestPostCommandAction(CmdAction):

    def run(self, cmd: Command) -> CmdActionResponse:
        response = CmdActionResponse(True, 'You can not run this cmd. Sorry')
        return response
