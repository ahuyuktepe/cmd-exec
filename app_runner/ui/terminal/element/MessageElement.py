import curses
from xml.etree.ElementTree import Element
from app_runner.app.context.AppContext import AppContext
from app_runner.events.EventManager import EventManager
from app_runner.events.UIEventType import UIEventType
from app_runner.ui.terminal.element.UIElement import UIElement
from app_runner.ui.terminal.enums.UIColor import UIColor
from app_runner.ui.terminal.utils.XmlElementUtil import XmlElementUtil
from app_runner.utils.StrUtil import StrUtil


class MessageElement(UIElement):

    def __init__(self, id: str, appContext: AppContext):
        super().__init__(id, 'message', appContext)

    # Event Listeners

    def showMessage(self, data: dict):
        msg = data.get('msg')
        type = data.get('type')
        self.__displayMessage(msg, type)

    # Setter Methods

    def setListeners(self):
        EventManager.listenEvent(UIEventType.SHOW_MESSAGE, self)

    def setAttributes(self, element: Element):
        parent = self.getParent()
        # Set Dimensions
        width = XmlElementUtil.getAttrValueAsInt(element, 'width', parent.getWidth())
        height = XmlElementUtil.getAttrValueAsInt(element, 'height', parent.getHeight())
        self.setDimensions(width, height)
        # Set Locations
        self.setLocation(2, 1)
        super().setAttributes(element)

    # Private Methods

    def __displayMessage(self, text: str, type: str = 'info'):
        text = StrUtil.getAlignedAndLimitedStr(text, self.getWidth()-3, 'left')
        if type == 'error':
            self._window.addstr(self._y, self._x, text, curses.color_pair(UIColor.ERROR_MESSAGE_COLOR))
        elif type == 'warning':
            self._window.addstr(self._y, self._x, text, curses.color_pair(UIColor.WARNING_MESSAGE_COLOR))
        elif type == 'success':
            self._window.addstr(self._y, self._x, text, curses.color_pair(UIColor.SUCCESS_MESSAGE_COLOR))
        else:
            self._window.addstr(self._y, self._x, text)
        self.refresh()
