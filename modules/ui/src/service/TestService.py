from src.service.AppService import AppService
from src.service.ConfigurationService import ConfigurationService


class TestService(AppService):
    __configService: ConfigurationService

    def __init__(self, configService: ConfigurationService):
        self.__configService = configService

    def printAppName(self):
        name = self._contextManager.getConfig('application.name')
        print('Name: ' + name)
