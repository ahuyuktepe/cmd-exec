from cmd_exec.service.TerminalService import TerminalService

from cmd_exec.service.DatabaseService import DatabaseService
from cmd_exec.command.CmdExecutor import CmdExecutor
from cmd_exec.command.CmdRequest import CmdRequest
from modules.sample.src.classes.User import User


class SampleCmdExecutor(CmdExecutor):

    def runCommand(self, request: CmdRequest):
        # Fetch TerminalService
        terminalService: TerminalService = request.terminalService
        # Fetch DatabaseService
        databaseService: DatabaseService = self._contextManager.getService('databaseService')
        databaseService.connect()
        # Add User
        user = User()
        user.addValue('first_name', 'New Test')
        user.addValue('last_name', 'User')
        databaseService.insert(user)
        # Print Users
        # self.__printUsers(databaseService)
        # Delete User
        user = User()
        user.addValue('first_name', 'New Test')
        databaseService.delete(user)
        # Print Users
        self.__printUsers(databaseService, terminalService)

    def __printUsers(self, databaseService: DatabaseService, terminalService: TerminalService):
        # Print Users
        user = User()
        users = databaseService.list(user)
        if users is not None:
            for user in users:
                terminalService.print('[red]' + user.toString())
