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
from app_runner.utils.StrUtil import StrUtil


class FieldService(BaseService):

    def getFieldValues(self, cmd: Command) -> dict:
        cid: str = cmd.getId()
        values: dict = {}
        defaultValuesFromConfig: dict = self._appContext.getConfig('main').getDefaultArgsByCommand(cid)
        values.update(defaultValuesFromConfig)
        fields: dict = cmd.getFields()
        defaultFieldValues: dict = self.getDefaultFieldValues(fields)
        values.update(defaultFieldValues)
        fieldValues: dict = self._appContext.getService('argumentService').getArgsAsDict(cid)
        values.update(fieldValues)
        return values

    def validateFieldValues(self, cmd: Command, fieldValues: dict):
        for fid, field in cmd.getFields().items():
            value = fieldValues.get(fid)
            if field.hasCustomValidator():
                package: str = 'modules.{module}.src.validators'.format(module=cmd.getModule())
                validator: str = field.getValidator()
                props: dict = StrUtil.getClassMethodMapFromStr(validator, 'validate')
                cls = ObjUtil.getClassFromStr(package, props.get('class'))
                validator = cls()
                validator.setAppContext(self._appContext)
                method: object = getattr(validator, props.get('method'))
                method(field, value)
            field.validate(value)

    def insertFields(self, cmd: Command, fields: list):
        if fields is not None:
            for fieldsProperties in fields:
                fieldType = fieldsProperties.get('type')
                ErrorUtil.raiseExceptionIfNone(fieldType, 'Type property of field is None.')
                field = self.__getFieldByType(fieldType, fieldsProperties)
                if field.hasOptions():
                    self.setFieldOptions(field, cmd.getModule(), fieldsProperties.get('options'))
                cmd.addField(field)

    def __getFieldByType(self, fieldType: str, fieldProps: dict) -> Field:
        if fieldType == 'number':
            return NumberField(fieldProps)
        elif fieldType == 'text':
            return TextField(fieldProps)
        elif fieldType == 'single_select':
            return SingleSelectField(fieldProps)
        elif fieldType == 'multi_select':
            return MultiSelectField(fieldProps)
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

    def setFieldOptions(self, field: Field, mid: str, options: list):
        if field.hasOptionGetter():
            package: str = 'modules.{module}.src.getters'.format(module=mid)
            props: dict = StrUtil.getClassMethodMapFromStr(field.getOptionGetter(), 'getOptions')
            cls = ObjUtil.getClassFromStr(package, props.get('class'))
            optGetter = cls()
            optGetter.setAppContext(self._appContext)
            getterMethod: object = getattr(optGetter, props.get('method'))
            opts = getterMethod(field)
            field.setOptions(opts)
        else:
            self.setOptions(options)

    def getDefaultFieldValues(self, fields: dict) -> dict:
        retDict: dict = {}
        field: Field
        for fid, field in fields.items():
            if field.hasDefaultValue():
                retDict[fid] = field.getDefault()
        return retDict
