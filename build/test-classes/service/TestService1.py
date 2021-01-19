from modules.test.src.service.TestService import TestService
from src.service.AppService import AppService


class TestService1(AppService):
    __sid: str
    __service: TestService

    def __init__(self, sid: str, testService: TestService):
        self.__sid = sid
        self.__service = testService

    def getId(self) -> str:
        return self.__sid

    def getService(self) -> TestService:
        return self.__service
