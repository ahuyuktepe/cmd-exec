import curses
import threading
from app_runner.classes.UIPrintArea import UIPrintArea
from app_runner.events.EventManager import EventManager
from app_runner.events.FlowEventType import FlowEventType
from app_runner.events.KeyEventType import KeyEventType
from app_runner.services.LogService import LogService
from app_runner.utils.ErrorUtil import ErrorUtil


class KeyboardListener:
    __printArea: UIPrintArea = None
    __keyboardListenerThread: object = None
    __logService: LogService
    __exitWhile: bool

    def __init__(self, printArea: UIPrintArea, logService: LogService):
        self.__printArea = printArea
        self.__logService = logService
        self.__exitWhile = False

    # Flow Methods

    def listen(self):
        if self.__keyboardListenerThread is None:
            # Listen Keyboard
            self.__keyboardListenerThread = threading.Thread(target=self.__listenKeyboard)
            self.__keyboardListenerThread.start()

    # Private Methods

    def __listenKeyboard(self):
        try:
            curses.cbreak()
            curses.noecho()
            window = self.__printArea.getWindow()
            while not self.__exitWhile:
                input = window.get_wch()
                if input == 'w':
                    EventManager.triggerEvent(KeyEventType.UP_KEY_PRESSED)
                elif input == 's':
                    EventManager.triggerEvent(KeyEventType.DOWN_KEY_PRESSED)
                elif input == 'a':
                    EventManager.triggerEvent(KeyEventType.LEFT_KEY_PRESSED)
                elif input == 'd':
                    EventManager.triggerEvent(KeyEventType.RIGHT_KEY_PRESSED)
                elif input == 'e':
                    EventManager.triggerEvent(KeyEventType.ENTER_KEY_PRESSED)
                elif input == ' ':
                    EventManager.triggerEvent(KeyEventType.SPACE_KEY_PRESSED)
                elif ord(input) == ord('\t'):
                    EventManager.triggerEvent(FlowEventType.FOCUS_ON_NEXT_ELEMENT)
                elif input == 'q':
                    EventManager.triggerEvent(FlowEventType.QUIT_APPLICATION)
                    self.__exitWhile = True
        except Exception as exp:
            ErrorUtil.handleException(exp, self.__logService)
