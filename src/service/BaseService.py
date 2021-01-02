from src.context.AppContext import AppContext
from src.context.ContextAware import ContextAware


class BaseService(ContextAware):
    _appContext: AppContext

    # Setter Methods

    def setAppContext(self, appContext: AppContext):
        self._appContext = appContext
