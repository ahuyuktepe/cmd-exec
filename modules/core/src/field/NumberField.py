from src.field.Field import Field
from src.field.FieldType import FieldType


class NumberField(Field):

    def __init__(self, fid: str):
        super().__init__(fid, FieldType.NUMBER)

    def validate(self):
        print('validating NumberField')

    def print(self):
        print("====================================== Number Field =========================================")
        print("--- Common Properties ---")
        super().print()
