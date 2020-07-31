from app_runner.services.BaseService import BaseService


class SampleService(BaseService):

    def print(self):
        print('Print SampleService')
        self._appContext.getService('logService').info('Print SampleService')
