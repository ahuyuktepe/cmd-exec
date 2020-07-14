from classes.services.LogService import LogService

class BaseService:
    _logService: LogService

    def setLogService(self, logService: LogService):
        self._logService = logService
