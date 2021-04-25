from cmd_exec.classes.MarkupBuilder import MarkupBuilder
from cmd_exec.command.CmdResponse import CmdResponse
from cmd_exec.service.TerminalService import TerminalService
from cmd_exec.service.DatabaseService import DatabaseService
from cmd_exec.command.CmdExecutor import CmdExecutor
from cmd_exec.command.CmdRequest import CmdRequest
from modules.sample.src.classes.User import User


class SampleCmdExecutor(CmdExecutor):

    def runCommand(self, request: CmdRequest) -> CmdResponse:
        response: CmdResponse = CmdResponse(True, 'view')
        builder: MarkupBuilder = MarkupBuilder()
        builder.addHorizontalTable([
            {'label': 'Column 1', 'length': 30},
            {'label': 'Column 2', 'length': 10},
            {'label': 'Column 3', 'length': 20}
        ], [
            ['Test Value 1', 'Test Value 2', 'Test Value 3'],
            ['Test Value 1', 'Test Value 2', 'Test Value 3'],
            ['Test Value 1', 'Test Value 2', 'Test Value 3']
        ])
        builder.nextLine()
        builder.addVerticalTable([
            {'label': 'First Name', 'value': 'Test User 1'},
            {'label': 'Last Name', 'value': 'Test User 2'}
        ], 20, 30)
        text = builder.getMarkupText()
        response.setContent(text)
        return response

    def listUsers(self, databaseService: DatabaseService):
        results: list = databaseService.executeSelectQuery("SELECT * FROM users")
        for result in results:
            print(str(result))

    def addUser(self, databaseService: DatabaseService):
        user = User()
        user.addValue('first_name', 'This is the first name')
        user.addValue('last_name', 'This is the last name')
        databaseService.insert(user)

    def deleteUser(self, databaseService: DatabaseService):
        user = User()
        user.addValue('first_name', 'New Test')
        databaseService.delete(user)

    def removeAllUsers(self, databaseService: DatabaseService):
        databaseService.executeUpdateQuery("DELETE FROM users")

    def printUsers(self, databaseService: DatabaseService, terminalService: TerminalService):
        # Print Users
        user = User()
        users = databaseService.list(user)
        text: str = '''[rpt:36:-]\n| [red][txt:15:left:First Name][rst] | [red][txt:15:left:Last Name][rst]|\n[rpt:36:-][br]'''
        if users is not None:
            for user in users:
                firstName = user.getValue('first_name')
                lastName = user.getValue('last_name')
                text += '| [txt:15:left:' + firstName + '][rst] | [txt:15:left:' + lastName + ']|[br]'
        text += '[rpt:36:-]'
        terminalService.print(text)
