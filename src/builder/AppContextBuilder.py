from src.context.AppContext import AppContext


class AppContextBuilder:

    @staticmethod
    def buildBaseAppContext() -> AppContext:
        appContext = AppContext()
        appContext.initializeConfig('main')
        return appContext
