from app_runner.app.config.AppConfig import AppConfig
from app_runner.errors.FieldValidationErrors import FieldValidationErrors
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
from app_runner.utils.DataUtil import DataUtil
from app_runner.utils.ObjUtil import ObjUtil
from app_runner.utils.StrUtil import StrUtil
from app_runner.utils.ValidationUtil import ValidationUtil


class FieldService(BaseService):

    def buildFields(self, props: list, mid: str) -> list:
        fields: list = []
        if props is not None:
            for fieldProps in props:
                field: Field = self.__initializeField(fieldProps)
                if field.hasOptions():
                    self.__setFieldOptions(field, mid, fieldProps.get('options'))
                fields.append(field)
        return fields

    def getFieldValues(self, cmd: Command) -> dict:
        ValidationUtil.failIfCommandIsNone(cmd)
        cid: str = cmd.getId()
        fields: dict = cmd.getFields()
        values: dict = {}
        if not DataUtil.isNullOrEmpty(fields):
            mainConfig: AppConfig = self._appContext.getConfig('main')
            defaultValuesFromConfig: dict = mainConfig.getObjValue('command_locators.' + cid + '.arguments')
            if not DataUtil.isNullOrEmpty(defaultValuesFromConfig):
                values.update(defaultValuesFromConfig)
            defaultFieldValues: dict = self.getDefaultFieldValues(fields)
            if not DataUtil.isNullOrEmpty(defaultFieldValues):
                values.update(defaultFieldValues)
            fieldValues: dict = self._appContext.getService('argumentService').getArgsAsDict(cid)
            if not DataUtil.isNullOrEmpty(fieldValues):
                values.update(fieldValues)
        return values

    def getDefaultFieldValues(self, fields: dict) -> dict:
        retDict: dict = {}
        if not DataUtil.isNullOrEmpty(fields):
            field: Field
            for fid, field in fields.items():
                if field.hasDefaultValue():
                    retDict[fid] = field.getDefault()
        return retDict

    def validateFieldValues(self, cmd: Command, fieldValues: dict) -> FieldValidationErrors:
        errors: FieldValidationErrors = FieldValidationErrors()
        for fid, field in cmd.getFields().items():
            value = fieldValues.get(fid)
            if field.hasCustomValidator():
                mid: str = cmd.getModule()
                package: str = 'modules.{module}.src.validators'.format(module=mid)
                validator: str = field.getValidator()
                props: dict = StrUtil.getClassMethodMapFromStr(validator, 'validate')
                clsName: str = props.get('class')
                ValidationUtil.failIfClassNotDefined(mid, clsName, 'validators')
                cls = ObjUtil.getClassFromStr(package, clsName)
                validator = cls()
                validator.setAppContext(self._appContext)
                classPath: str = package + "." + clsName
                methodName: str = props.get('method')
                ValidationUtil.failIfClassMethodDoesNotExist(validator, classPath, methodName)
                method: object = getattr(validator, methodName)
                method(field, value, errors)
            field.validate(value, errors)
        return errors

    # Private Methods

    def __initializeField(self, props: dict) -> Field:
        fieldType: str = props.get('type')
        if fieldType == 'number':
            return NumberField(props)
        elif fieldType == 'text':
            return TextField(props)
        elif fieldType == 'single_select':
            return SingleSelectField(props)
        elif fieldType == 'multi_select':
            return MultiSelectField(props)
        elif fieldType == 'date':
            return DateField(props)
        elif fieldType == 'datetime':
            return DateTimeField(props)
        elif fieldType == 'file':
            return FileField(props)
        elif fieldType == 'directory':
            return DirectoryField(props)
        else:
            return Field(props)

    def __setFieldOptions(self, field: Field, mid: str, options: list):
        if field.hasOptionGetter():
            package: str = 'modules.{module}.src.getters'.format(module=mid)
            props: dict = StrUtil.getClassMethodMapFromStr(field.getOptionGetter(), 'getOptions')
            clsName: str = props.get('class')
            ValidationUtil.failIfClassNotDefined(mid, clsName, 'getters')
            cls = ObjUtil.getClassFromStr(package, clsName)

            optGetter = cls()
            classPath: str = package + "." + clsName
            methodName: str = props.get('method')
            ValidationUtil.failIfClassMethodDoesNotExist(optGetter, classPath, methodName)

            optGetter.setAppContext(self._appContext)
            getterMethod: object = getattr(optGetter, methodName)
            opts = getterMethod(field)
            field.setOptions(opts)
        else:
            field.setOptions(options)
