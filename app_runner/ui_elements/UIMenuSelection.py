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
        self._printArea.listenUserSelection(self)

    # Utility Methods

    def destroy(self):
        curses.unget_wch('q')

    # Event Handlers

    def upKeyPressed(self):
        EventManager.triggerEvent(UIEventType.UP_KEY_PRESSED)

    def downKeyPressed(self):
        EventManager.triggerEvent(UIEventType.DOWN_KEY_PRESSED)

    def leftKeyPressed(self):
        EventManager.triggerEvent(UIEventType.LEFT_KEY_PRESSED)

    def rightKeyPressed(self):
        EventManager.triggerEvent(UIEventType.RIGHT_KEY_PRESSED)

    def enterKeyPressed(self):
        EventManager.triggerEvent(UIEventType.ENTER_KEY_PRESSED)

    def displayPreviousMenus(self):
        EventManager.triggerEvent(UIEventType.DISPLAY_PREVIOUS_MENUS)
