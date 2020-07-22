from app_runner.app.AppContext import AppContext
from app_runner.app.MainAppConfig import MainAppConfig
from app_runner.services.CommandService import CommandService
from app_runner.services.FieldService import FieldService
from app_runner.services.LogService import LogService


class TestBaseService:
    _appContext: AppContext
    _menu: dict = {
        "id": "main",
        "name": "Main Menu",
        "commands": [
            {
                "id": "test-cmd",
                "description": "Test Command",
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
        }
    }

    def _initAppContext(self):
        mainAppConfig = MainAppConfig(self._test_config)
        self._appContext = AppContext(mainAppConfig)
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
