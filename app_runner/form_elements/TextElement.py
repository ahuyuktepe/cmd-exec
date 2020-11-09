from app_runner.field.Field import Field
from app_runner.form_elements.FormUIElement import FormUIElement
from app_runner.utils.StrUtil import StrUtil


class TextElement(FormUIElement):
    def __init__(self, field: Field):
        super().__init__(field)
        self.__value = ""

    # Utility Methods

    def display(self):
        label = self._field.getLabel()
        if self.isSelected():
            label = u'\u00BB' + ' ' + label
        label = StrUtil.getAlignedAndLimitedStr(label, self.getWidth(), 'left')
        self._printArea.printText(1, 1, label)
        self._printArea.printLine(1, 3, 50)
        self.refresh()

    def getCalculatedHeight(self) -> int:
        return 4

    def getUserInput(self) -> object:
        return 'test'
