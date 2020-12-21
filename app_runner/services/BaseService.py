from app_runner.app.context.AppContext import AppContext
from app_runner.services.LogService import LogService

class BaseService:
    _appContext: AppContext

    # Setter Methods

    def setAppContext(self, appContext: AppContext):
        self._appContext = appContext

    # Utility Methods

    def log(self, level: str, msg: str, params: dict = {}):
        logService: LogService = self._appContext.getService('logService')
        if logService is not None:
            renderedMsg = msg.format(**params)
            if level == 'info':
                logService.info(renderedMsg)
            elif level == 'debug':
                logService.debug(renderedMsg)
            elif level == 'warn':
                logService.warn(renderedMsg)
            elif level == 'error':
                logService.error(renderedMsg)
