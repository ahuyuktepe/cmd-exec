import curses
from xml.etree.ElementTree import Element
from app_runner.events.EventManager import EventManager
from app_runner.events.UIEventType import UIEventType
from app_runner.ui_elements.UIElement import UIElement


class UIMenuSelection(UIElement):
    __text: str

    def __init__(self, id: str):
        super().__init__(id, 'menu-selection')

    # Setter Methods

    def setText(self, text: str):
        self.__text = text

    def setAttributes(self, element: Element):
        self.setText(element.text)
        super().setAttributes(element)

    def setListeners(self):
        EventManager.listenEvent(UIEventType.VIEW_LOADED, self)

    # Event Listeners

    def viewLoaded(self, data: dict):
        self.__listenUserInput()

    # Utility Methods

    def destroy(self):
        curses.unget_wch('q')

    # Private Methods

    def __listenUserInput(self):
        curses.cbreak()
        curses.noecho()
        input = None
        while input != 'q':
            input = self._printArea.getUserInputAsChar()
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
