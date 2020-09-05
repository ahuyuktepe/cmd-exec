from app_runner.ui.terminal.screen.UIScreen import UIScreen


class MainScreen(UIScreen):

    def __init__(self, title: str):
        UIScreen.__init__(self, 'main', title)
