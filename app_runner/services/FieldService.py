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
from app_runner.utils.FileUtil import FileUtil
from app_runner.utils.ObjUtil import ObjUtil
from app_runner.utils.StrUtil import StrUtil
from app_runner.utils.ValidationUtil import ValidationUtil


class FieldService(BaseService):

    # Utility Methods

    def buildFields(self, module: str, props: list) -> list:
        fields: list = []
        if props is not None:
            for fieldProps in props:
                field: Field = self.__initializeField(module, fieldProps)
                if field.hasOptions():
                    self.__setFieldOptions(field, fieldProps.get('options'))
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

    def validateFieldValues(self, cmd: Command, fieldValues: dict, errors: FieldValidationErrors = None) -> FieldValidationErrors:
        if errors is None:
            errors: FieldValidationErrors = FieldValidationErrors()
        for fid, field in cmd.getFields().items():
            value = fieldValues.get(fid)
            fieldErrors: FieldValidationErrors = self.validateFieldValue(field, value)
            errors.addErrors(fieldErrors.getErrors())
        return errors

    def validateFieldValue(self, field: Field, value: object) -> FieldValidationErrors:
        errors: FieldValidationErrors = FieldValidationErrors()
        if field.hasCustomValidator():
            validator: str = field.getValidator()
            props: dict = StrUtil.getClassMethodMapFromStr(validator, 'validate')
            clsName: str = props.get('class')
            mid: str = props.get('module')
            methodName: str = props.get('method')
            classPath: str = 'modules.{module}.src.validators.{className}'.format(module=mid, className=clsName)
            FileUtil.failIfClassFileDoesNotExist(mid, clsName, 'validators')
            cls = ObjUtil.getClassFromStr(classPath, clsName)
            validator = cls()
            validator.setAppContext(self._appContext)
            ValidationUtil.failIfClassMethodDoesNotExist(validator, classPath, methodName)
            method: object = getattr(validator, methodName)
            method(field, value, errors)
        field.validate(value, errors)
        return errors

    # Private Methods

    def __initializeField(self, module: str, props: dict) -> Field:
        fieldType: str = props.get('type')
        if fieldType == 'number':
            field = NumberField(props)
        elif fieldType == 'text':
            field = TextField(props)
        elif fieldType == 'single_select':
            field = SingleSelectField(props)
            field.setOptionGetter(module, props.get('getter'))
        elif fieldType == 'multi_select':
            field = MultiSelectField(props)
            field.setOptionGetter(module, props.get('getter'))
        elif fieldType == 'date':
            field = DateField(props)
        elif fieldType == 'datetime':
            field = DateTimeField(props)
        elif fieldType == 'file':
            field = FileField(props)
        elif fieldType == 'directory':
            field = DirectoryField(props)
        else:
            field = Field(props)
        field.setValidator(module, props.get('validator'))
        return field

    def __setFieldOptions(self, field: Field, options: list):
        if field.hasOptionGetter():
            props: dict = StrUtil.getClassMethodMapFromStr(field.getOptionGetter(), 'getOptions')
            mid = props['module']
            clsName: str = props.get('class')
            getterClassPath: str = 'modules.{module}.src.getters.{className}'.format(module=mid, className=clsName)
            FileUtil.failIfClassFileDoesNotExist(mid, clsName, 'getters')
            cls = ObjUtil.getClassFromStr(getterClassPath, clsName)

            optGetter = cls()
            methodName: str = props.get('method')
            ValidationUtil.failIfClassMethodDoesNotExist(optGetter, getterClassPath, methodName)

            optGetter.setAppContext(self._appContext)
            getterMethod: object = getattr(optGetter, methodName)
            opts = getterMethod(field)
            field.setOptions(opts)
        else:
            field.setOptions(options)
