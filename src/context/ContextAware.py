from src.context.AppContext import AppContext


class ContextAware:
    _appContext: AppContext

    def setAppContext(self, appContext: AppContext):
        self._appContext = appContext
