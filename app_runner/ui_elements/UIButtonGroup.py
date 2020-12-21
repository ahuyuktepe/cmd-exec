import math
from xml.etree.ElementTree import Element
from app_runner.classes.RecordPaginator import RecordPaginator
from app_runner.classes.UIPrintArea import UIPrintArea
from app_runner.enums.UIColor import UIColor
from app_runner.events.EventManager import EventManager
from app_runner.events.FlowEventType import FlowEventType
from app_runner.ui_elements.UIElement import UIElement
from app_runner.utils.StrUtil import StrUtil
from app_runner.utils.XmlElementUtil import XmlElementUtil


class UIButtonGroup(UIElement):
    __recordPaginator: RecordPaginator
    __btnWidth: int

    def __init__(self, id: str):
        super().__init__(id, 'button')
        self.__recordPaginator = None

    # Setter Functions

    def setAttributes(self, element: Element):
        # Set Common Attributes
        super().setAttributes(element)
        self.__btnWidth = XmlElementUtil.getAttrValueAsInt(element, 'btn-width', 10)

    def setButtons(self, buttons: list):
        maxCount = math.floor(self.getWidth() / self.__btnWidth)
        self.__recordPaginator = RecordPaginator(buttons, maxCount)

    def listenEvents(self):
        EventManager.listenEvent(FlowEventType.ADD_BUTTON, self)

    # Utility Methods

    def display(self):
        x = 2
        y = 1
        # Print Previous Page Icon If Applicable
        if self.__recordPaginator.hasPreviousPage():
            self._printArea.printText(x, y, u'\u00AB')
            x += 2
        index = 0
        for btnProps in self.__recordPaginator.getRecordsInPage():
            text = '[' + StrUtil.getAlignedAndLimitedStr(btnProps['label'], (self.__btnWidth - 2), 'center') + ']'
            if index == self.__recordPaginator.getActiveIndex():
                self._printArea.printText(x, y, text, UIColor.ACTIVE_COMMAND_COLOR)
            else:
                self._printArea.printText(x, y, text)
            x += len(text) + 2
            index += 1
        if self.__recordPaginator.hasNextPage():
            self._printArea.printText(x, y, u'\u00BB')
            x += 2
        self.refresh()

    def focus(self):
        self.__recordPaginator.setActiveIndex(0)
        self.display()

    def unfocus(self):
        self.__recordPaginator.setActiveIndex(-1)
        self.display()

    # Event Listeners

    def addButton(self, data):
        self.__recordPaginator.addRecord({
            'id': data.get('id'),
            'event': data.get('event'),
            'label': data.get('label')
        })
        self.display()

    def enterKeyPressed(self, data):
        activeBtn = self.__recordPaginator.getActiveRecord()
        evnt = activeBtn['event']
        EventManager.triggerEvent(evnt)

    def leftKeyPressed(self, data):
        self.__recordPaginator.moveToPreviousRecord()
        self.display()

    def rightKeyPressed(self, data):
        self.__recordPaginator.moveToNextRecord()
        self.display()
