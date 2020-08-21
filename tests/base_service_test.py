from app_runner.app.AppContext import AppContext
from app_runner.services.CommandService import CommandService
from app_runner.services.FieldService import FieldService
from app_runner.services.LogService import LogService

class TestBaseService:
    _appContext: AppContext
    _menu: dict = {
        "id": "test",
        "name": "Test Menu",
        "commands": [
            {
                "id": "test-cmd",
                "description": "Test Command",
                "executor": 'TestExecutor.executeTestCmd',
                "fields": [
                    {"id": "first-name", "label": "First Name", "type": "text"},
                    {"id": "last-name", "label": "Last Name", "type": "text", "default": "User"},
                    {"id": "email", "label": "Email", "type": "text", "required": True}
                ]
            }
        ]
    }
    _test_config = {
        "name": "Test Application Name",
        "log_settings": {
            "level": "info",
            "dir_path": "args",
            "file_name": "test-logs"
        },
        'command_locators': {
            'test': {
                'cmd': 'test-cmd',
                'module': 'test-module',
                'menu': 'test-menu'
            }
        }
    }

    def _initAppContext(self):
        self._appContext = AppContext()
        # LogService
        obj: dict = self._appContext.getConfig('main').getObjValue('log_settings')
        self._appContext.addService('logService', LogService(obj))
        # CommandService
        cmdService: CommandService = CommandService()
        cmdService.setAppContext(self._appContext)
        self._appContext.addService('commandService', cmdService)
        # FieldService
        fieldService: FieldService = FieldService()
        fieldService.setAppContext(self._appContext)
        self._appContext.addService('fieldService', fieldService)