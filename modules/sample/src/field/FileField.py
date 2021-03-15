from src.field.TextField import TextField


class FileField(TextField):

    def __init__(self, id: str):
        super().__init__(id)

    def print(self):
        print("=======================================================================================================")
        print('FileField => id: ' + self._id + ' | type: ' + self._type + ' | label: ' + self._label)
        print('Value: ' + str(self._value))
