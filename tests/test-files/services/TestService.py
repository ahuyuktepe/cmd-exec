from service.AppService import AppService


class TestService(AppService):

    def getName(self) -> str:
        return 'TestService'
