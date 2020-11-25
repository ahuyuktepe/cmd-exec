from app_runner.classes.HtmlPrinter import HtmlPrinter
from app_runner.events.EventManager import EventManager
from app_runner.events.UIEventType import UIEventType
from app_runner.ui_elements.UIElement import UIElement


class UIHtml(UIElement):
    __htmlPrinter: HtmlPrinter
    __start: int
    __end: int
    __maxRowCount: int
    __isListeningUserInput: bool

    def __init__(self, id: str):
        super().__init__(id, 'html')
        self.__isListeningUserInput = False

    # Event Listeners

    def displayHtml(self, data: dict = {}):
        self.__start = 0
        self.__end = self.getHeight() - 2
        htmlText = data.get('html')
        self.__htmlPrinter = HtmlPrinter(htmlText, self._printArea)
        self.__htmlPrinter.printLines(self.__start, self.__end)
        self.__maxRowCount = self.__htmlPrinter.getY()
        self.refresh()
        if not self.__isListeningUserInput:
            self.__fetchUserInput()

    def updateText(self, data: dict = {}):
        self.clear()
        self.displayHtml(data)

    # Private Methods

    def __fetchUserInput(self):
        self.__isListeningUserInput = True
        exitWhile = False
        while not exitWhile:
            selection = self._printArea.getUserInputAsChar()
            if selection == 'q':
                exitWhile = True
            elif selection == 's' and self.__hasNextLine():
                # Move Next Line
                self.__start += 1
                self.__end += 1
                self.__htmlPrinter.printLines(self.__start, self.__end)
            elif selection == 'w' and self.__hasPreviousLine():
                # Move Previous Line
                self.__start -= 1
                self.__end -= 1
                self.__htmlPrinter.printLines(self.__start, self.__end)
            elif selection == 'e':
                EventManager.triggerEventByElementId(UIEventType.UPDATE_TEXT, 'response-html', {
                    'html': '<html><label>Testing</label></html>'
                })
        self.__isListeningUserInput = False

    def __hasPreviousLine(self) -> bool:
        return self.__start > 0

    def __hasNextLine(self) -> bool:
        return self.__end <= self.__maxRowCount

    # Utility Methods

    def setListeners(self):
        EventManager.listenEvent(UIEventType.DISPLAY_HTML, self)
        EventManager.listenEvent(UIEventType.UPDATE_TEXT, self)
