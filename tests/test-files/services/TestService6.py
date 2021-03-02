from src.service.AppService import AppService


class TestService6(AppService):
    __name: str
    __testService: object
    __testService3: object

    def __init__(self, name: str, service: object, service3: object):
        self.__name = name
        self.__testService = service
        self.__testService3 = service3

    def getDescription(self):
        return "name: " + self.__name + " | testService: " + self.__testService.getName() + \
               " | testService3: " + self.__testService3.getServiceName()
