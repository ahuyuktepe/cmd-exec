from src.context.AppContext import AppContext


class CmdExecApp:
    _appContext: AppContext

    def __init__(self, context: AppContext):
        self._appContext = context

    def run(self):
        print('Running')