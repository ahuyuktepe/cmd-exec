from app_runner.app.config.AppConfig import AppConfig
from app_runner.app.context.AppContext import AppContext


class TestConfigUtil:

    @staticmethod
    def getMainCmdLocator(appContext: AppContext, cid: str) -> str:
        appConfig: AppConfig = appContext.getConfig('main')
        cmdLocator: dict = appConfig.getObjValue('command_locators.' + cid)
        return cmdLocator
