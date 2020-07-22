from app_runner.field.DateField import DateField
from app_runner.field.DateTimeField import DateTimeField
from app_runner.field.DirectoryField import DirectoryField
from app_runner.field.Field import Field
from app_runner.field.FileField import FileField
from app_runner.field.MultiSelectField import MultiSelectField
from app_runner.field.NumberField import NumberField
from app_runner.field.SingleSelectField import SingleSelectField
from app_runner.field.TextField import TextField
from app_runner.menu.Command import Command
from app_runner.services.BaseService import BaseService
from app_runner.utils.ErrorUtil import ErrorUtil
from app_runner.utils.ObjUtil import ObjUtil

class FieldService(BaseService):

    def validateFieldValues(self, fields: dict, fieldValues: dict):
        for fid, field in fields.items():
            value = fieldValues.get(fid)
            if field.hasCustomValidator():
                validator = ObjUtil.getClassFromStr('validators', field.getValidator())
                obj = validator()
                obj.validate(field, value)
            else:
                field.validate(value)

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
            field = SingleSelectField(fieldProps)
            field.populateOptions(
                fieldProps.get('getter'),
                fieldProps.get('options')
            )
            return field
        elif fieldType == 'multi_select':
            field = MultiSelectField(fieldProps)
            field.populateOptions(
                fieldProps.get('getter'),
                fieldProps.get('options')
            )
            return field
        elif fieldType == 'date':
            return DateField(fieldProps)
        elif fieldType == 'datetime':
            return DateTimeField(fieldProps)
        elif fieldType == 'file':
            return FileField(fieldProps)
        elif fieldType == 'directory':
            return DirectoryField(fieldProps)
        else:
            return Field(fieldProps)
