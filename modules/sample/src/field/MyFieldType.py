from cmd_exec.field.Field import Field


class MyFieldType(Field):
    def __init__(self, id: str):
        super().__init__(id, 'my_field_type')
