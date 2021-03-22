from src.classes.TextColor import TextColor
from src.field.DateField import DateField
from src.field.Field import Field
from src.field.SelectionField import SelectionField
from src.field.TextField import TextField
from src.service.AppService import AppService

class TerminalService(AppService):
    __textColorCodes: list = [TextColor.RED, TextColor.BLUE, TextColor.CYAN, TextColor.GREEN, TextColor.RESET, TextColor.BOLD]

    def print(self, text: str):
        parsedText = self.__parseText(text)
        print(parsedText)

    def setFieldValueByUserInput(self, field: Field):
        if field.isText():
            self.__setTextFieldValue(field)
        elif field.isSelection():
            self.__setSelectionFieldValue(field)
        elif field.isDate():
            self.__setDateFieldValue(field)
        return field

    def __setDateFieldValue(self, field: DateField):
        label = '\n' + field.getLabel() + ':\n'
        label += '(' + field.getFormat() + ') > '
        label = self.__parseText(label)
        value = input(label)
        field.setValue(value)

    def __setSelectionFieldValue(self, field: SelectionField):
        label = '\n' + field.getLabel()
        options = field.getOptions()
        label = label + ':\n'
        for option in options:
            label += '\t - ' + option.getId() + ': ' + option.getValue() + '\n'
        label += '> '
        label = self.__parseText(label)
        value = input(label)
        field.setValue(value)

    def __setTextFieldValue(self, field: TextField):
        label = '\n' + field.getLabel() + ':\n> '
        label = self.__parseText(label)
        value = input(label)
        field.setValue(value)

    def __parseText(self, text: str):
        parsedText = text
        for colorCode in TerminalService.__textColorCodes:
            parsedText = parsedText.replace(('#' + colorCode['id'] + '#'), colorCode['code'])
        return parsedText
