import curses
from xml.etree.ElementTree import Element
from app_runner.app.context.AppContext import AppContext
from app_runner.events.EventManager import EventManager
from app_runner.events.UIEventType import UIEventType
from app_runner.field.Field import Field
from app_runner.menu.Command import Command
from app_runner.ui.terminal.element.UIElement import UIElement
from app_runner.ui.terminal.utils.XmlElementUtil import XmlElementUtil
from app_runner.utils.StrUtil import StrUtil


class FormElement(UIElement):

    def __init__(self, id: str, appContext: AppContext):
        super().__init__(id, 'form', appContext)

    # Setter Methods

    def setAttributes(self, element: Element):
        parent = self.getParent()
        # Set Dimensions
        width = XmlElementUtil.getAttrValueAsInt(element, 'width', parent.getWidth())
        height = XmlElementUtil.getAttrValueAsInt(element, 'height', parent.getHeight())
        self.setDimensions(width, height)
        # Set Locations
        self.setLocation(0, 0)
        super().setAttributes(element)

    def setListeners(self):
        EventManager.listenEvent(UIEventType.VIEW_LOADED, self)
        EventManager.listenEvent(UIEventType.EXECUTE_COMMAND, self)

    # Event Listeners

    def executeCommand(self, data: dict):
        print('execute')
        cmd: Command = data.get('command')
        fields: list = list(cmd.getFields().values())
        field: Field
        y = 5
        for field in fields:
            text = StrUtil.getAlignedAndLimitedStr(field.getLabel(), 15, 'left')
            self._window.addstr(y, 2, text + ':')
            y += 2
        self.refresh()


    def viewLoaded(self, data: dict):
        self.__listenUserInput()

    # Utility Methods

    def print(self):
        print('print')
        self.refresh()

    # Private Methods

    def __listenUserInput(self):
        curses.nocbreak()
        input = self._window.getstr(1, 1).decode('utf-8')
        print('listenUserInput : ' + input)
