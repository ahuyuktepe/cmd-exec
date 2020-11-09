from app_runner.field.Field import Field
from app_runner.ui_elements.UIElement import UIElement


class FormUIElement(UIElement):
    _field: Field
    _selected: bool

    def __init__(self, field: Field):
        super().__init__(field.getId(), 'form-element')
        self._field = field
        self._selected = False

    # Getter Method

    def getCalculatedHeight(self) -> int:
        return 5

    def getUserInput(self) -> object:
        return None

    def getFieldId(self) -> str:
        return self._field.getId()

    def isSelected(self) -> bool:
        return self._selected

    # Setter Methods

    def setSelected(self, selected: bool):
        self._selected = selected
