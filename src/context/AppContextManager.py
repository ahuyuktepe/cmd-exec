from src.context.AppContext import AppContext


class AppContextManager:
    __appContext: AppContext

    def __init__(self, appContext: AppContext):
        self.__appContext = appContext

    # Getter Methods

    def getConfig(self, key: str):
        return self.__appContext.getConfig(key)

    def getService(self, sid: str):
        return self.__appContext.getService(sid)
