from service.AppService import AppService


class TestService3(AppService):
    __testService: object

    def __init__(self, testService):
        self.__testService = testService

    def getServiceName(self) -> str:
        name = self.__testService.getName()
        return name
