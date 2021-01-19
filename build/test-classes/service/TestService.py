from src.service.AppService import AppService


class TestService(AppService):
    __id: str

    def __init__(self, sid: str):
        self.__sid = sid

    def getId(self) -> str:
        return self.__sid
