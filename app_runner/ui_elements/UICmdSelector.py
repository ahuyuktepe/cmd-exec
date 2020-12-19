from xml.etree.ElementTree import Element
from app_runner.events.EventManager import EventManager
from app_runner.events.UIEventType import UIEventType
from app_runner.menu.Menu import Menu
from app_runner.ui_elements.UICmdMenu import UICmdMenu
from app_runner.ui_elements.UIElement import UIElement
from app_runner.ui_elements.UITopMenu import UITopMenu


class UICmdSelector(UIElement):
    __topNavMenu: UITopMenu
    __cmdMenu: UICmdMenu
    __topMenuNameWidth: int
    __menus: list

    def __init__(self, id: str):
        super().__init__(id, 'menu')

    # Setter Methods

    def setAttributes(self, element: Element):
        super().setAttributes(element)

    def setCmdMenu(self, cmdMenu: UICmdMenu):
        self.__cmdMenu = cmdMenu

    def setTopMenu(self, topMenu: UITopMenu):
        self.__topNavMenu = topMenu

    def setMenus(self, menus: list):
        self.__menus = menus

    # Utility Methods

    def display(self):
        self.__topNavMenu.displayMenus({
            'menus': self.__menus
        })
        self.__displayActiveMenuCommands()

    def setListeners(self):
        EventManager.listenEvent(UIEventType.LEFT_KEY_PRESSED, self)
        EventManager.listenEvent(UIEventType.RIGHT_KEY_PRESSED, self)
        EventManager.listenEvent(UIEventType.UP_KEY_PRESSED, self)
        EventManager.listenEvent(UIEventType.DOWN_KEY_PRESSED, self)
        EventManager.listenEvent(UIEventType.ENTER_KEY_PRESSED, self)
        EventManager.listenEvent(UIEventType.DISPLAY_MENUS, self)
        EventManager.listenEvent(UIEventType.DISPLAY_PREVIOUS_MENUS, self)

    # Event Listeners

    def displayPreviousMenus(self, data):
        self.__topNavMenu.movePreviousMenus()
        self.__displayActiveMenuCommands()

    def displayMenus(self, data: dict):
        self.__topNavMenu.displayMenus(data)
        self.__displayActiveMenuCommands()

    def enterKeyPressed(self, data):
        cmd = self.__cmdMenu.getActiveCommand()
        EventManager.triggerEvent(UIEventType.COMMAND_SELECTED, {
            'command': cmd
        })

    def upKeyPressed(self, data):
        self.__cmdMenu.moveUp()

    def downKeyPressed(self, data):
        self.__cmdMenu.moveDown()

    def leftKeyPressed(self, data):
        self.__topNavMenu.moveLeft()
        self.__displayActiveMenuCommands()

    def rightKeyPressed(self, data):
        self.__topNavMenu.moveRight()
        self.__displayActiveMenuCommands()

    # Private Methods

    def __displayActiveMenuCommands(self):
        menu: Menu = self.__topNavMenu.getActiveMenu()
        self.__cmdMenu.displayCommandsInMenu(menu)
