import curses
from app_runner.events.UIEventType import UIEventType


class UIPrintArea:
    __window: object
    __isListeningUserInput: bool
    _width: int
    _height: int

    def __init__(self, window: object, width: int, height: int):
        self.__window = window
        self._width = width
        self._height = height
        self.__isListeningUserInput = False

    def printText(self, x: int, y: int, text: str, colorCode: int = 0):
        if colorCode == 0:
            self.__window.addstr(y, x, text)
        else:
            self.__window.addstr(y, x, text, curses.color_pair(colorCode))

    def printTextViaDict(self, values: dict):
        colorCode = values.get('colorCode')
        if colorCode is None:
            self.__window.addstr(values.get('y'), values.get('x'), values.get('text'))
        else:
            self.__window.addstr(values.get('y'), values.get('x'), values.get('text'), curses.color_pair(colorCode))

    def printLine(self, x: int, y: int, width: int):
        self.__window.hline(y, x, curses.ACS_HLINE, width)

    def addBorder(self):
        self.__window.border()

    def refresh(self):
        return self.__window.refresh()

    def clear(self):
        return self.__window.clear()

    # Utility Methods

    def move(self, x: int, y: int):
        self.__window.mvderwin(y, x)
        self.refresh()

    def moveCursor(self, x: int, y: int):
        self.__window.move(y, x)
        self.refresh()

    # Getter Methods

    def listenUserSelection(self, handler):
        if self.__isListeningUserInput:
            return
        curses.cbreak()
        curses.noecho()
        methodName: str = None
        exitWhile = False
        while not exitWhile:
            input = self.__window.get_wch()
            if input == 'w':
                methodName = UIEventType.UP_KEY_PRESSED
            elif input == 's':
                methodName = UIEventType.DOWN_KEY_PRESSED
            elif input == 'a':
                methodName = UIEventType.LEFT_KEY_PRESSED
            elif input == 'd':
                methodName = UIEventType.RIGHT_KEY_PRESSED
            elif input == 'e':
                methodName = UIEventType.ENTER_KEY_PRESSED
            elif input == 'r':
                methodName = UIEventType.DISPLAY_PREVIOUS_MENUS
            elif input == 'q':
                methodName = UIEventType.QUIT_KEY_PRESSED
            elif input == ' ':
                methodName = UIEventType.MULTI_CHOICE_OPTION_SELECTED
            if hasattr(handler, methodName):
                method = getattr(handler, methodName)
                response = method()
                if response is not None:
                    exitWhile = response
                elif input == 'q':
                    exitWhile = True

    def getUserInputAsStr(self, x: int, y: int) -> object:
        curses.echo()
        input = self.__window.getstr(y, x)
        return input.decode('utf-8')

    def getWidth(self) -> int:
        return self._width

    def getHeight(self) -> int:
        return self._height

    def getWindow(self) -> object:
        return self.__window

    # Utility Methods

    def getCursorLocation(self) -> dict:
        location = self.__window.getyx()
        return {
            'y': location[0],
            'x': location[1]
        }

    def scroll(self, lines: int):
        self.__window.scroll(lines)
        self.refresh()
