from app_runner.ui_elements.TerminalScreen import TerminalScreen


class TerminalService:
    __screen: TerminalScreen = None

    def __init__(self, screen: TerminalScreen):
        self.__screen = screen

    def displayScreen(self):
        self.__screen.start()

    def displayView(self, data: dict = {}):
        self.__screen.displayView(data)
