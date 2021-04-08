from cmd_exec.service.AppService import AppService
from cmd_exec.service.ConfigurationService import ConfigurationService


class SampleService(AppService):

    def printAppName(self):
        configService: ConfigurationService = self._contextManager.getService('configService')
        name = configService.getValue('application.name')
        print("App Name: " + name)