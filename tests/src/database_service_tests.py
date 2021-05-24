from cmd_exec.builder.AppContextBuilder import AppContextBuilder
from cmd_exec.context.AppContext import AppContext
from cmd_exec.context.AppContextManager import AppContextManager
from cmd_exec.service.DatabaseService import DatabaseService
from tests.src.utils.TestUtil import TestUtil

class TestDatabaseService:
    databaseService: DatabaseService

    def setup_method(self, method):
        TestUtil.setupTestingEnvironment()
        TestUtil.useConfigFilesInConfigsDir(['main.config.yaml'])
        TestUtil.useDatabaseFilesInConfigsDir(['test-database.db'])
        TestUtil.buildModuleFiles('test', {
            'name': 'test',
            'version': '0.0.1'
        })
        TestUtil.useClassFileInModule(['TestUser.py'], 'test')
        appContext: AppContext = AppContextBuilder.buildBaseAppContext()
        contextManager: AppContextManager = AppContextManager(appContext)
        self.databaseService = contextManager.getService('databaseService')

    def teardown_method(self, method):
        TestUtil.destroyTestingEnvironment()

    def test_insert(self):
        from modules.test.src.classes.TestUser import TestUser
        user: TestUser = TestUser()
        user.addValue('first_name', 'Test')
        user.addValue('last_name', 'User')
        self.databaseService.insert(user)
        sql = "SELECT * FROM users"
        results = self.databaseService.executeSelectQuery(sql)
        count = len(results)
        assert count == 1

    def test_delete(self):
        from modules.test.src.classes.TestUser import TestUser
        user: TestUser = TestUser()
        user.addValue('first_name', 'Test')
        user.addValue('last_name', 'User')
        self.databaseService.insert(user)
        self.databaseService.delete(user)
        sql = "SELECT * FROM users"
        results = self.databaseService.executeSelectQuery(sql)
        count = len(results)
        assert count == 0

    def test_list(self):
        from modules.test.src.classes.TestUser import TestUser
        user: TestUser = TestUser()
        user.addValue('first_name', 'Test')
        user.addValue('last_name', 'User')
        self.databaseService.insert(user)
        self.databaseService.insert(user)
        results = self.databaseService.list(user)
        count = len(results)
        assert count == 2

    def test_custom_sql_execution(self):
        sql: str = "INSERT INTO users VALUES ('Test', 'User')"
        self.databaseService.executeUpdateQuery(sql)
        sql = "SELECT * FROM users"
        results = self.databaseService.executeSelectQuery(sql)
        count = len(results)
        assert count == 1
