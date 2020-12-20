from app_runner.events.EventManager import EventManager
from app_runner.events.UIEventType import UIEventType
from app_runner.ui_elements.TerminalScreen import TerminalScreen


class TerminalService:
    __screen: TerminalScreen = None

    def __init__(self, screen: TerminalScreen):
        self.__screen = screen

    def displayScreen(self):
        self.__screen.start()

    def displayView(self, data):
        self.__screen.displayView(data)

    def displayHtml(self, html: str):
        self.__screen.displayView({'vid': 'html'})
        EventManager.triggerEvent(UIEventType.DISPLAY_XML, {'html': html})

    def displayMessage(self, text: str):
        self.__screen.displayMessage(text)
