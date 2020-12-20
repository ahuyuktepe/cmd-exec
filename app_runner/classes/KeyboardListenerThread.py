import curses
import sys
import threading
from app_runner.classes.UIPrintArea import UIPrintArea
from app_runner.events.EventManager import EventManager
from app_runner.events.UIEventType import UIEventType
from app_runner.services.LogService import LogService


class KeyboardListenerThread:
    __printArea: UIPrintArea = None
    __keyboardListenerThread: object = None
    __logService: LogService

    def __init__(self, printArea: UIPrintArea, logService: LogService):
        self.__printArea = printArea
        self.__logService = logService

    def listen(self):
        if self.__keyboardListenerThread is None:
            # Listen Keyboard
            self.__keyboardListenerThread = threading.Thread(target=self.__listenKeyboard)
            self.__keyboardListenerThread.start()

    def __listenKeyboard(self):
        try:
            curses.cbreak()
            curses.noecho()
            exitWhile = False
            window = self.__printArea.getWindow()
            while not exitWhile:
                input = window.get_wch()
                if input == 'w':
                    EventManager.triggerEvent(UIEventType.UP_KEY_PRESSED)
                elif input == 's':
                    EventManager.triggerEvent(UIEventType.DOWN_KEY_PRESSED)
                elif input == 'a':
                    EventManager.triggerEvent(UIEventType.LEFT_KEY_PRESSED)
                elif input == 'd':
                    EventManager.triggerEvent(UIEventType.RIGHT_KEY_PRESSED)
                elif input == 'e':
                    EventManager.triggerEvent(UIEventType.ENTER_KEY_PRESSED)
                elif input == 'r':
                    EventManager.triggerEvent(UIEventType.DISPLAY_PREVIOUS_MENUS)
                elif input == 'q':
                    EventManager.triggerEvent(UIEventType.QUIT_KEY_PRESSED)
                    exitWhile = True
                elif input == 'z':
                    EventManager.triggerEvent(UIEventType.RETURN_TO_MENU_VIEW)
                elif input == ' ':
                    EventManager.triggerEvent(UIEventType.MULTI_CHOICE_OPTION_SELECTED)
        except Exception as exp:
            raise exp