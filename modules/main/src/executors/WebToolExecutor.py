from app_runner.extension.ContextAware import ContextAware


class WebToolExecutor(ContextAware):

    def getName(self, values: dict):
        print("WebToolExecutor.getName")