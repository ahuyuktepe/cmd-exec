from app_runner.extension.ContextAware import ContextAware
from modules.main.src.services.SampleService import SampleService


class WebToolExecutor(ContextAware):

    def getName(self, values: dict):
        print("WebToolExecutor.getName")
        print("Values: " + str(values))
        self._appContext.getService('logService').info('WebToolExecutor')
        service: SampleService = self._appContext.getService('main.SampleService')
        service.print()
