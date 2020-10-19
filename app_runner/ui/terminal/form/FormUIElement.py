from app_runner.app.context.AppContext import AppContext
from app_runner.field.Field import Field
from app_runner.ui.terminal.element.UIElement import UIElement


class FormUIElement(UIElement):
    _field: Field

    def __init__(self, field: Field, appContext: AppContext):
        super().__init__(field.getId(), 'form-element', appContext)
        self._field = field

    # Getter Methods

    def getId(self) -> str:
        return self._field.getId()

    def getUserInput(self) -> object:
        pass
