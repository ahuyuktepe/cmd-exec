from src.action.CmdAction import CmdAction
from src.action.CmdActionResponse import CmdActionResponse
from src.menu.Command import Command
import getpass

class TestPreCommandAction(CmdAction):

    def run(self, cmd: Command) -> CmdActionResponse:
        allowedUsers = self._context.getConfig('security.allowed_users')
        print("Allowed Users: " + str(allowedUsers))
        username = getpass.getuser()
        print("Username: " + str(username))
        status = username in allowedUsers
        response = CmdActionResponse(status, 'You can not run this cmd. Sorry')
        return response
