from app_runner.enums.UIColor import UIColor
from app_runner.errors.FieldValidationErrors import FieldValidationErrors
from app_runner.field.Field import Field
from app_runner.services.FieldService import FieldService
from app_runner.ui_elements.UIElement import UIElement
from app_runner.utils.StrUtil import StrUtil


class FormUIElement(UIElement):
    _field: Field
    _mid: str
    _fieldService: FieldService
    _fieldValidationErrors: FieldValidationErrors
    _selected: bool
    _value: object

    def __init__(self, field: Field, mid: str, fieldService: FieldService):
        super().__init__(field.getId(), 'form-element')
        self._field = field
        self._mid = mid
        self._fieldService = fieldService
        self._selected = False
        self._fieldValidationErrors =  FieldValidationErrors()

    # Getter Method

    def getCalculatedHeight(self) -> int:
        return 5

    def getCalculatedWidth(self) -> int:
        return self.getWidth()

    def getUserInput(self) -> object:
        return None

    def getFieldId(self) -> str:
        return self._field.getId()

    def isSelected(self) -> bool:
        return self._selected

    # Setter Methods

    def setSelected(self, selected: bool):
        self._selected = selected

    # Utility Methods

    def validate(self):
        self._fieldValidationErrors = self._fieldService.validateFieldValue(self._field, self._mid, self._value)

    def getValidationErrors(self) -> FieldValidationErrors:
        return self._fieldValidationErrors

    def hasErrors(self) -> bool:
        return self._fieldValidationErrors.hasErrors()

    def printValidationErrors(self, y: int):
        count = 1
        for error in self._fieldValidationErrors.getErrors():
            y += 1
            msg = '  * ' + error.getMsg()
            msg = StrUtil.getAlignedAndLimitedStr(msg, self.getWidth(), 'left')
            self._printArea.printText(1, y, msg, UIColor.ERROR_MESSAGE_COLOR)
            if count == 5:
                break
            count += 1
