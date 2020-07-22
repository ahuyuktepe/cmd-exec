from app_runner.app.AppConfig import AppConfig

class MainAppConfig(AppConfig):

    def __init__(self, configs: dict):
        super().__init__(configs)
