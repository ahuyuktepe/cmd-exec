from app_runner.app.AppContext import AppContext

class ContextAware:
    _appContext: AppContext

    def setAppContext(self, appContext: AppContext):
        self._appContext = appContext
