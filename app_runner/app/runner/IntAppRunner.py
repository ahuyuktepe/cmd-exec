from app_runner.app.context.AppContext import AppContext
from app_runner.app.runner.ApplicationRunner import ApplicationRunner
from app_runner.ui.terminal.element.UIScreen import UIScreen


class IntAppRunner(ApplicationRunner):
    __screen: UIScreen

    def __init__(self, context: AppContext):
        super().__init__(context)
        self.__screen = context.getScreen()

    def run(self):
        self.__screen.displayView('menu')
        self.__screen.listenUserInput()
