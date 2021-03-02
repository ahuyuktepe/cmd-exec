from src.service.AppService import AppService


class TestService1(AppService):

    def getAppName(self) -> str:
        name = self._contextManager.getConfig('application.name')
        return name
