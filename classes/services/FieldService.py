from classes.field.Field import Field
from classes.field.MultiSelectField import MultiSelectField
from classes.field.NumberField import NumberField
from classes.field.SingleSelectField import SingleSelectField
from classes.field.TextField import TextField
from classes.menu.Command import Command
from classes.utils.ErrorUtil import ErrorUtil

class FieldService:

    def validateFieldValues(self, fields: dict, fieldValues: dict):
        for fid, field in fields.items():
            field.validate(fieldValues.get(fid))
        pass

    def insertFields(self, cmd: Command, fields: list):
        if fields is not None:
            for fieldsProperties in fields:
                fieldType = fieldsProperties.get('type')
                ErrorUtil.raiseExceptionIfNone(fieldType, 'Type property of field is None.')
                cmd.addField(self.__getFieldByType(fieldType, fieldsProperties))

    def __getFieldByType(self, fieldType: str, fieldProps: dict) -> Field:
        if fieldType == 'number':
            return NumberField(fieldProps)
        elif fieldType == 'text':
            return TextField(fieldProps)
        elif fieldType == 'single_select':
            return SingleSelectField(fieldProps)
        elif fieldType == 'multi_select':
            return MultiSelectField(fieldProps)
        else:
            return Field(fieldProps)
