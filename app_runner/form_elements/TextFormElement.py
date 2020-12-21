from app_runner.enums.UIColor import UIColor
from app_runner.events.EventManager import EventManager
from app_runner.events.FlowEventType import FlowEventType
from app_runner.field.Field import Field
from app_runner.form_elements.FormElement import FormUIElement
from app_runner.services.FieldService import FieldService
from app_runner.utils.StrUtil import StrUtil


class TextElement(FormUIElement):

    def __init__(self, field: Field, fieldService: FieldService):
        super().__init__(field, fieldService)
        self._value = None

    # Utility Methods

    def display(self):
        label = self._field.getLabel()
        if self.isSelected():
            label = u'\u00BB' + ' ' + label
        label = StrUtil.getAlignedAndLimitedStr(label, self.getWidth(), 'left')
        y = 1
        # Print Label
        self._printArea.printText(1, y, label)
        # Print Validation Errors
        self.printValidationErrors(y)
        # User Entry Line
        y = self.getCalculatedHeight() - 2
        self._printArea.printText(1, y, '.' * 50)
        if self._value is not None:
            self._printArea.printText(1, y, self._value)
        self.refresh()

    def getCalculatedHeight(self) -> int:
        return 4 + self._fieldValidationErrors.getErrorCount()

    def collectUserInput(self):
        y = self.getCalculatedHeight() - 2
        self._value = self._printArea.getUserInputAsStr(1, y)
        self.clear()
        self.display()
        EventManager.triggerEvent(FlowEventType.FORM_ELEMENT_VALUE_ENTERED)
