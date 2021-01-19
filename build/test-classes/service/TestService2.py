from modules.test.src.service.TestService import TestService
from modules.test.src.service.TestService1 import TestService1
from src.service.AppService import AppService


class TestService2(AppService):
    __sid: str
    __service: TestService
    __service1: TestService1

    def __init__(self, sid: str, testService: TestService, testService1: TestService1):
        self.__sid = sid
        self.__service = testService
        self.__service1 = testService1

    def getId(self) -> str:
        return self.__sid

    def getService(self) -> TestService:
        return self.__service

    def getService1(self) -> TestService1:
        return self.__service1
