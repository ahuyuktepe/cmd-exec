from app_runner.services.BaseService import BaseService
from modules.main.src.utils.SampleUtil import SampleUtil


class SampleService(BaseService):

    def print(self):
        print('Print SampleService')
        self._appContext.getService('logService').info('Print SampleService')
        SampleUtil.test()
