from app_runner.enums.UIColor import UIColor
from app_runner.errors.FieldValidationErrors import FieldValidationErrors
from app_runner.field.Field import Field
from app_runner.services.FieldService import FieldService
from app_runner.ui_elements.UIElement import UIElement
from app_runner.utils.StrUtil import StrUtil


class FormUIElement(UIElement):
    _field: Field
    _fieldService: FieldService
    _fieldValidationErrors: FieldValidationErrors
    _selected: bool
    _value: object
    _maxErrorLineCount: int = 4

    def __init__(self, field: Field, fieldService: FieldService):
        super().__init__(field.getId(), 'form-element')
        self._field = field
        self._fieldService = fieldService
        self._selected = False
        self._fieldValidationErrors = FieldValidationErrors()

    # Getter Method

    def getCalculatedHeight(self) -> int:
        return 5

    def getCalculatedWidth(self) -> int:
        return self.getWidth()

    def collectUserInput(self):
        return None

    def getFieldId(self) -> str:
        return self._field.getId()

    def getValue(self) -> object:
        return self._value

    def getErrorLineCount(self) -> int:
        errorCount = self._fieldValidationErrors.getErrorCount()
        if errorCount > self._maxErrorLineCount:
            return self._maxErrorLineCount
        return errorCount

    # Query Methods

    def isSelected(self) -> bool:
        return self._selected

    # Setter Methods

    def setSelected(self, selected: bool):
        self._selected = selected

    # Utility Methods

    def validate(self):
        fieldValue = self.getValue()
        self._fieldValidationErrors = self._fieldService.validateFieldValue(self._field, fieldValue)

    def getValidationErrors(self) -> FieldValidationErrors:
        return self._fieldValidationErrors

    def hasErrors(self) -> bool:
        return self._fieldValidationErrors.hasErrors()

    def printValidationErrors(self, y: int):
        maxErrorCount: int = self.getErrorLineCount()
        for i in range(0, maxErrorCount):
            y += 1
            error = self._fieldValidationErrors.getErrorByIndex(i)
            msg = '  * '
            if i == (self._maxErrorLineCount - 1):
                msg += '...'
            else:
                msg += error.getMsg()
                msg = StrUtil.getAlignedAndLimitedStr(msg, self.getWidth(), 'left')
            self._printArea.printText(1, y, msg, UIColor.ERROR_MESSAGE_COLOR)
