from app_runner.app.AppConfig import AppConfig
from app_runner.extension.ContextAware import ContextAware
from modules.sample.src.services.SampleService import SampleService


class WebToolExecutor(ContextAware):

    def getName(self, values: dict):
        print("WebToolExecutor.getName")
        print("Values: " + str(values))
        self._appContext.getService('logService').info('WebToolExecutor')
        service: SampleService = self._appContext.getService('sample.SampleService')
        service.print()
        config: AppConfig = self._appContext.getConfig('main.sample1')
        firstName: str = config.getObjValue('full-name.first')
        lastName: str = config.getObjValue('full-name.last')
        print('First Name : ' + firstName + ' | Last Name : ' + lastName)
