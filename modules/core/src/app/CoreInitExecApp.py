from src.app.CmdExecApp import CmdExecApp


class CoreInitExecApp(CmdExecApp):
    def run(self):
        print('Running application via CoreInitExecApp')
        modes = self._contextManager.getConfig('application.modes')
        print('Modes: ' + str(modes))
