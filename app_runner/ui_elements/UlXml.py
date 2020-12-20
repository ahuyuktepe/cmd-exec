from app_runner.classes.XmlPrinter import XmlPrinter
from app_runner.events.EventManager import EventManager
from app_runner.events.UIEventType import UIEventType
from app_runner.ui_elements.UIElement import UIElement


class UIHtml(UIElement):
    __xmlPrinter: XmlPrinter
    __maxRowCount: int
    __start: int
    __end: int
    __currentY: int

    def __init__(self, id: str):
        super().__init__(id, 'html')
        self.__start = 0

    # Event Listeners

    def displayXml(self, data: dict = {}):
        self.__end = self._printArea.getHeight()
        htmlText = data.get('html')
        self.__xmlPrinter = XmlPrinter(htmlText, self._printArea)
        self.printLines()

    def printLines(self):
        self.clear()
        y = 0
        for i in range(self.__start, self.__end):
            self.__xmlPrinter.printLine(i, y)
            y += 1
        self.refresh()

    def updateText(self, data: dict = {}):
        self.clear()
        self.displayXml(data)

    # Listener Methods

    def upKeyPressed(self, data):
        if self.__xmlPrinter.hasLine(self.__start - 1):
            # Move Previous Line
            self.__start -= 1
            self.__end -= 1
            self.printLines()

    def downKeyPressed(self, data):
        if self.__xmlPrinter.hasLine(self.__end):
            # Move Next Line
            self.__start += 1
            self.__end += 1
            self.printLines()

    # Utility Methods

    def setListeners(self):
        EventManager.listenEvent(UIEventType.DISPLAY_XML, self)
        EventManager.listenEvent(UIEventType.UPDATE_TEXT, self)
        EventManager.listenEvent(UIEventType.UP_KEY_PRESSED, self)
        EventManager.listenEvent(UIEventType.DOWN_KEY_PRESSED, self)
