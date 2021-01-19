from app_runner.app.context.AppContext import AppContext
from app_runner.services.ArgumentService import ArgumentService
from app_runner.services.CommandService import CommandService
from app_runner.services.FieldService import FieldService
from app_runner.services.LogService import LogService
from temp.utils.TestFileUtil import TestFileUtil


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
                'menu': 'test-menu',
                'arguments': {
                    'first-name': 'test',
                    'last-name': 'user'
                }
            }
        }
    }

    def _initAppContext(self):
        self.__createConfigFiles()
        self._appContext = AppContext()
        # LogService
        obj: dict = self._appContext.getConfig('core').getObjValue('log_settings')
        self._appContext.addService('logService', LogService(obj))
        # CommandService
        cmdService: CommandService = CommandService()
        cmdService.setAppContext(self._appContext)
        self._appContext.addService('commandService', cmdService)
        # FieldService
        fieldService: FieldService = FieldService()
        fieldService.setAppContext(self._appContext)
        self._appContext.addService('fieldService', fieldService)
        # ArgumentService
        self._appContext.addService('argumentService', ArgumentService())

    def __createConfigFiles(self):
        TestFileUtil.createMainConfig(self._test_config)
        TestFileUtil.createModuleConfig('core', 'core', self._menu)
