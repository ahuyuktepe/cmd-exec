from app_runner.app.context.AppContext import AppContext
from app_runner.errors.FieldValidationErrors import FieldValidationErrors
from app_runner.field.Field import Field
from app_runner.menu.Command import Command
from app_runner.services.FieldService import FieldService
from app_runner.ui.terminal.element.UIElement import UIElement


class FormUIElement(UIElement):
    _value: object
    _field: Field
    _errors: FieldValidationErrors
    _fieldService: FieldService

    def __init__(self, field: Field, appContext: AppContext):
        super().__init__(field.getId(), 'form-element', appContext)
        self._field = field
        self._fieldService = appContext.getService('fieldService')

    # Getter Methods

    def getId(self) -> str:
        return self._field.getId()

    def getUserInput(self) -> object:
        pass

    # Utility Methods

    def validate(self, cmd: Command) -> FieldValidationErrors:
        self._errors = self._fieldService.validateFieldValue(self._field, cmd.getModule(), self._value)
        return self._errors
