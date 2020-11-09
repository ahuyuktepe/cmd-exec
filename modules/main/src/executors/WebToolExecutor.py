from app_runner.extension.ContextAware import ContextAware
from app_runner.services.UIService import TerminalService


class WebToolExecutor(ContextAware):

    def getName(self, values: dict):
        print("WebToolExecutor.getName")
        # Display command response
