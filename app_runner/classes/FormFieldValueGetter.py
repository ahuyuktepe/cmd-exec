import threading

from app_runner.form_elements import FormElement


class FormFieldValueGetter:
    __thread: object

    def __init__(self):
        self.__thread = None

    def getValue(self, formElement: FormElement):
        if self.__thread is None:
            # Listen Keyboard
            self.__thread = threading.Thread(target=formElement.getUserInput)
            self.__thread.start()
