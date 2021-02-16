from src.field.Field import Field
from src.field.FieldType import FieldType


class TextField(Field):

    def __init__(self, fid: str):
        super().__init__(fid, FieldType.TEXT)

    def validate(self):
        print('validating TextField')

    def print(self):
        print("====================================== Text Field =========================================")
        print("--- Common Properties ---")
        super().print()
